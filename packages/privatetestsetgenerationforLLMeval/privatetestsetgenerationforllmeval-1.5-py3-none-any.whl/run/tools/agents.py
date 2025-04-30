import os
import random
import csv
import numpy as np
from typing import Any
from dotenv import load_dotenv, find_dotenv
from presidio_analyzer import AnalyzerEngine

from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from sklearn.cluster import KMeans
_ = load_dotenv(find_dotenv())

# Environment variables
openai_api_key = os.getenv("AZURE_OPENAI_KEY")
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
azure_openai_endpoint = os.getenv("AZURE_ENDPOINT")
gpt_4_model_deployment_name = os.getenv("GPT_4_MODEL_DEPLOYMENT_NAME", "GPT-4")
embedding_deployment_name = os.getenv("EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002")

###############################################################################
# 1) DIVERSITY AUGMENTING AGENT
###############################################################################
def diversity_augmenting_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    1) Reads 'D' (list of {text, embedding}).
    2) Runs KMeans for 10 clusters, picks up to 5 samples each.
    4) Returns 'topic_vectorstore' in the pipeline state.
    """
    embedded_data = state.get("D", [])
    if not embedded_data:
        print("No data found in state['D']. Skipping clustering.")
        return {**state, "topic_vectorstore": None}

    # Extract embeddings + text
    embeddings = np.array([item["embedding"] for item in embedded_data])
    texts = [item["text"] for item in embedded_data]
    
    # K-Means clustering
    num_clusters = 10
    print(f"Performing K-Means with {num_clusters} clusters on {len(embeddings)} embeddings.")
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(embeddings)

    # Group indices by cluster
    cluster_map = {}
    for idx, label in enumerate(labels):
        cluster_id = int(label)
        cluster_map.setdefault(cluster_id, []).append(idx)

    cluster_docs = []
    for cluster_id, indices in cluster_map.items():
        if not indices:
            continue
        rep_idx = random.choice(indices)
        rep_text = texts[rep_idx]

        # Up to 5 random samples
        sample_count = min(len(indices), 5)
        chosen_indices = random.sample(indices, sample_count)
        combined_samples = [texts[i] for i in chosen_indices]

        # Generate a cluster title
        cluster_title = _generate_cluster_title(rep_text)

        doc_content = "\n---\n".join(combined_samples)
        doc = Document(
            page_content=doc_content,
            metadata={"cluster_id": cluster_id, "title": cluster_title}
        )
        cluster_docs.append(doc)

    # Build a Chroma store
    topic_vectorstore = build_vectorstore_from_docs(cluster_docs)

    # Explicitly clear the topic_vectorstore after each run to avoid carry-over
    print("\n===== DIVERSITY AGENT OUTPUT =====")
    for d in cluster_docs:
        print(f"Cluster ID: {d.metadata['cluster_id']}, Title: {d.metadata['title']}")
    print("==================================\n")

    # Clear vector store after the run
    #state["topic_vectorstore"] = None  # Ensuring the vector store is cleaned

    return {**state, "topic_vectorstore": topic_vectorstore}

def _generate_cluster_title(sample_text: str) -> str:
    """
    Use GPT-4 to create a short descriptive title for a cluster.
    """
    prompt_template = PromptTemplate.from_template(
        """
        You are a clustering assistant. The following is a short excerpt from one cluster:
        {sample_text}

        Provide a concise (3-7 words) title that best represents the overall topic or domain.
        No additional commentary, just the title.
        """
    )
    llm = AzureChatOpenAI(
        api_key=openai_api_key,
        api_version=openai_api_version,
        deployment_name=gpt_4_model_deployment_name,
        model_name="gpt-4-32k",
    )
    chain = prompt_template | llm
    response = chain.invoke({"sample_text": sample_text[:1000]})
    return response.content.strip()

def build_vectorstore_from_docs(docs: list[Document]):
    """
    """
    from langchain_openai import AzureOpenAIEmbeddings
    from langchain.vectorstores import Chroma

    azure_embedder = AzureOpenAIEmbeddings(
        openai_api_key=openai_api_key,
        azure_deployment=embedding_deployment_name
    )

    return Chroma.from_documents(
        docs,
        azure_embedder,
        collection_name="clustered_docs",
    )


_ = load_dotenv(find_dotenv())



###############################################################################
# PRIVACY AGENT:
###############################################################################


def privacy_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Analyzes the document to identify sensitive entities (PII) and flags them for pseudonymization.
    Generates a privacy analysis report with the main sensitive entities and KPIs.
    """
    topic_vectorstore = state.get("topic_vectorstore", None)
    if not topic_vectorstore:
        print("No topic_vectorstore found. Skipping.")
        return {**state, "privacy_analysis_report": "No topics to analyze."}

    # Initialize Presidio Analyzer
    analyzer = AnalyzerEngine()

    # Retrieve documents from the vector store
    docs = topic_vectorstore.similarity_search("ALL CLUSTERS", k=50)

    # Analyze the documents for sensitive entities using Presidio NER
    sensitive_entities = {}
    total_entities = 0
    combined_text = ""

    # Define the entities we want to detect
    entity_types = [
        "PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD", "BANK_ACCOUNT", 
        "DATE_TIME", "LOCATION", "IP_ADDRESS", "CREDIT_CARD", "MEDICAL_INFORMATION"
    ]

    for d in docs:
        text = d.page_content
        combined_text += text + "\n\n"

        # Use Presidio to analyze the text
        results = analyzer.analyze(text=text, entities=entity_types, language='en')

        # Count and store the detected entities
        for result in results:
            entity_type = result.entity_type
            sensitive_entities[entity_type] = sensitive_entities.get(entity_type, 0) + 1
            total_entities += 1

    # Generate the privacy analysis report
    report = f"""
    Privacy Analysis Report
    -----------------------
    Total Sensitive Entities Found: {total_entities}

    Breakdown by Entity Type:
    """
    
    for entity_type, count in sensitive_entities.items():
        report += f"\n- {entity_type}: {count}"

    report += f"""

    Documents Analyzed: {len(docs)}
    """
    print(report)

    return {**state, "privacy_analysis_report": report, "D_priv": combined_text}




###############################################################################
# 3) SYNTHETIC DATA GENERATOR
###############################################################################
def synthetic_data_generator(state: dict[str, Any]) -> dict[str, Any]:
    """
    1) Reads 'D_priv' (the sanitized text).
    2) Reads 'qa_count' from state to determine how many Q&A pairs to generate.
    3) Generates Q&A pairs referencing the sanitized text, saves to CSV, returns final report.
    """
    D_priv = state.get("D_priv", "")
    if not D_priv:
        return {**state, "D_synth": "No data to synthesize."}

    # If user didn't specify a count, default to 10
    qa_count = state.get("qa_count", 10)  # user may override this

    # Prompt GPT to generate Q&A pairs
    prompt_template = PromptTemplate.from_template(f"""
    You are the Synthetic Data Generation Agent. We have a sanitized domain text:

    {{sanitized_text}}

    Please:
    1) Craft exactly {qa_count} Q&A pairs that test a chatbot's understanding of this sanitized domain text.
    2) Provide each Q&A as "Q: ... A: ...".
    3) Additionally, explain (in 1-2 paragraphs) the procedure used to form these Q&A samples,
       including how you ensured coverage of domain aspects and how the sanitized text influenced it.

    Output Format:
    - Title: "Synthetic Data Generation Report"
    - Section: "Procedure for QA Sample Generation"
    - Section: "QA Pairs" ({qa_count} pairs, each with 'Q:' and 'A:')
    """)
    llm = AzureChatOpenAI(
        api_key=openai_api_key,
        api_version=openai_api_version,
        deployment_name=gpt_4_model_deployment_name,
        model_name="gpt-4-32k",
    )
    chain = prompt_template | llm
    response = chain.invoke({"sanitized_text": D_priv})
    synthesis_report = response.content.strip()

    # Parse out the Q&As from the text
    qa_pairs = _extract_qa_pairs(synthesis_report)

    # Save Q&As to CSV
    csv_filename = "qa_pairs" +str(qa_count) +".csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Answer"])
        for (q, a) in qa_pairs:
            writer.writerow([q, a])

    print(f"Saved {qa_count} Q&A pairs to '{csv_filename}'.")

    final_report = (
        f"{synthesis_report}\n\n"
        f"(Note: Q&A pairs have been extracted and saved to '{csv_filename}'.)"
    )
    return {**state, "D_synth": final_report}

def _extract_qa_pairs(text: str) -> list[tuple[str, str]]:
    """
    A naive approach to parse lines containing "Q: ..." and "A: ...".
    Returns a list of (question, answer) tuples.
    """
    lines = text.split("\n")
    qa_pairs = []
    current_q = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Q:"):
            current_q = stripped[2:].strip()
        elif stripped.startswith("A:") and current_q:
            answer = stripped[2:].strip()
            qa_pairs.append((current_q, answer))
            current_q = None

    return qa_pairs
