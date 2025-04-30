import unittest
from unittest.mock import patch
import numpy as np
import sys
from pathlib import Path
src_path = Path(__file__).parent.parent / 'src/run/tools/'
sys.path.append(str(src_path))


from agents import diversity_augmenting_agent, privacy_agent, synthetic_data_generator

class TestAgentFunctions(unittest.TestCase):


    def test_privacy_agent_with_no_vectorstore(self):
        # Simulate state without a vectorstore
        state = {}

        result = privacy_agent(state)

        self.assertEqual(result["privacy_analysis_report"], "No topics to analyze.")

    def test_synthetic_data_generator_with_missing_data(self):
        # Simulate state with no sanitized text (D_priv)
        state = {}

        result = synthetic_data_generator(state)

        self.assertEqual(result["D_synth"], "No data to synthesize.")

if __name__ == '__main__':
    unittest.main()
