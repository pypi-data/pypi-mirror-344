import os
import re
import csv
import numpy as np
import sys
from pathlib import Path
src_path = Path(__file__).parent.parent / 'src/tools/'
sys.path.append(str(src_path))
from typing import TypedDict
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END

from pypdf import PdfReader
from openai import AzureOpenAI
from tools.graph import create_graph

_ = load_dotenv(find_dotenv()) 

# Basic Azure config from your environment (adjust as needed)
openai_api_key = os.getenv("AZURE_OPENAI_KEY")
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

# The deployment name for the embedding model
EMBEDDING_DEPLOYMENT_NAME = os.getenv("EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002")

class PipelineInput(TypedDict):
    """
    The user input state for the pipeline:
      - file_path: Path to a PDF file
    """
    file_path: str
    continue_pipeline: bool

def extract_sentences(text: str) -> list[str]:
    """
    Splits text into sentence-like units using a regex pattern.
    Filters out empty or non-alphanumeric sentences.
    """
    sentence_pattern = re.compile(r'(?<!\w\.\w)(?<![A-Z][a-z]\.)(?<=\.|\?|!)"?(?=\s|$)')
    raw_sentences = sentence_pattern.split(text)
    return [s.strip() for s in raw_sentences if s.strip() and re.search(r'\w', s)]

def load_pdf_as_sentences(file_path: str) -> list[str]:
    """
    Reads a PDF using PyPDF, concatenates all text, then extracts sentences.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return []

    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        text_on_page = page.extract_text() or ""
        full_text += text_on_page

    sentences = extract_sentences(full_text)
    print(f"Total sentences extracted: {len(sentences)}")
    return sentences

def embed_sentences_azure(sentences: list[str]) -> list[dict]:
    """
    1) Takes a list of sentences (strings).
    2) Calls Azure OpenAI embeddings endpoint (embeddings.create).
    3) Returns a list of dicts: [{'text': <sentence>, 'embedding': <np.array>}].
    """
    if not sentences:
        return []

    client = AzureOpenAI(
        api_key=openai_api_key,
        api_version=openai_api_version
    )

    print(f"Embedding {len(sentences)} sentences with model '{EMBEDDING_DEPLOYMENT_NAME}'...")
    response = client.embeddings.create(
        input=sentences,
        model=EMBEDDING_DEPLOYMENT_NAME
    )

    embedded_samples = []
    for sentence_text, embed_obj in zip(sentences, response.data):
        vec = np.array(embed_obj.embedding)
        embedded_samples.append({
            "text": sentence_text,
            "embedding": vec
        })

    return embedded_samples

def get_user_input(state: PipelineInput) -> PipelineInput:
    """
    Prompts the user for a PDF path. Type 'q' or an empty line to quit.
    """
    if state.get("file_path") == "":
        user_input = input("Enter the path to your PDF file (or 'q' to quit): ").strip()
        if user_input.lower() == 'q' or user_input == '':
            return {"file_path": "", "continue_pipeline": False}
        return {"file_path": user_input, "continue_pipeline": True}
    else:
        return {"file_path": "", "continue_pipeline": False}

def run_pipeline(state: PipelineInput):
    """
    Orchestrates the multi-agent pipeline with sentence-level embeddings from a PDF.
    1. Ask user for how many Q&A pairs to generate.
    2. Load the PDF as a list of sentences.
    3. Embed them via AzureOpenAI.
    4. Call the pipeline (Diversity -> Privacy -> Synthetic), passing 'qa_count'.
    5. Print final synthetic dataset.
    """
    if not state["file_path"]:
        print("No PDF file provided. Exiting.")
        return state

    # 1) Prompt user for how many Q&A pairs to generate
    user_input_count = input("How many Q&A pairs would you like to generate? (Default: 10): ")
    try:
        qa_count = int(user_input_count)
    except ValueError:
        qa_count = 10

    # 2) Load the PDF as sentences
    sentences = load_pdf_as_sentences(state["file_path"])
    if not sentences:
        print("No valid text from PDF or extraction failed.")
        return state

    # 3) Embed these sentences
    embedded_dataset = embed_sentences_azure(sentences)
    if not embedded_dataset:
        print("No valid data to embed.")
        return state

    # 4) Create and invoke the multi-agent pipeline
    workflow = create_graph()
    final_state = workflow.invoke({
        "D": embedded_dataset,
        "qa_count": qa_count  
    })

    # 5) Print final synthetic dataset
    print("\n--- Final Synthetic Dataset ---")
    synthetic_data = final_state.get("D_synth", "<No synthetic data found>")
    print(synthetic_data)
    print(f"If the pipeline completed successfully, {qa_count} Q&A pairs have been saved to 'qa_pairs.csv'.")

    return state

def create_main_graph() -> StateGraph:
    """
    Builds a simple graph with:
      1) get_input (prompt user for PDF path)
      2) run_pipeline (extract sentences, embed them, run pipeline)
    """
    workflow = StateGraph(PipelineInput)
    workflow.add_node("get_input", get_user_input)
    workflow.add_node("run_pipeline", run_pipeline)

    workflow.set_entry_point("get_input")

    workflow.add_conditional_edges(
        "get_input",
        lambda x: "continue" if x["continue_pipeline"] else "end",
        {
            "continue": "run_pipeline",
            "end": END
        }
    )

    workflow.add_edge("run_pipeline", "get_input")

    return workflow.compile()

def main():
    conversation_graph = create_main_graph()
    
    # Initialize the state with empty or default values
    initial_state = {"file_path": "", "continue_pipeline": True}
    
    # Execute the pipeline and stop asking for input after the first run
    conversation_graph.invoke(initial_state)

if __name__ == "__main__":
    main()
