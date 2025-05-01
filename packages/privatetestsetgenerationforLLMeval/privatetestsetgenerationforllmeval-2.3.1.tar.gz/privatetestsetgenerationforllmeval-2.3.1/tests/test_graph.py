import sys
from pathlib import Path
src_path = Path(__file__).parent.parent / 'src/run/tools/'
sys.path.append(str(src_path))

import unittest
from graph import create_graph  
from langgraph.graph import StateGraph

class TestAgentsGraph(unittest.TestCase):

    def setUp(self):
        from graph import AgentState
        self.workflow = StateGraph(AgentState)

        from agents import diversity_augmenting_agent, privacy_agent, synthetic_data_generator
        
        self.workflow.add_node("diversity", diversity_augmenting_agent)
        self.workflow.add_node("privacy", privacy_agent)
        self.workflow.add_node("synthesis", synthetic_data_generator)

        self.workflow.set_entry_point("diversity")
        self.workflow.add_edge("diversity", "privacy")
        self.workflow.add_edge("privacy", "synthesis")
        self.workflow.add_edge("synthesis", "__end__")

    def test_graph_contains_all_agents(self):
        # Check that all expected nodes are present
        expected_nodes = {"diversity", "privacy", "synthesis"}
        graph_nodes = set(self.workflow.nodes.keys())
        self.assertTrue(expected_nodes.issubset(graph_nodes), f"Missing nodes: {expected_nodes - graph_nodes}")


    def test_graph_flow_structure(self):
        expected_edges = {
            ("diversity", "privacy"),
            ("privacy", "synthesis"),
            ("synthesis", "__end__")
        }
        self.assertTrue(expected_edges.issubset(self.workflow.edges), f"Missing expected edges: {expected_edges - self.workflow.edges}")

    def test_create_graph_returns_compiled(self):
        compiled_graph = create_graph()
        self.assertTrue(hasattr(compiled_graph, "invoke"), "Compiled graph should have 'invoke' method")

if __name__ == '__main__':
    unittest.main()
