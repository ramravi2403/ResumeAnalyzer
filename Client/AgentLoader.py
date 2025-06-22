import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Server import AnalyzerAgent
from streamlit import cache_resource


class AgentLoader:

    _default_course_file = "./Server/downsized_dataset.csv"

    @classmethod
    @cache_resource
    def load(cls, agent_type: str):
        """
        Load a specified agent type, using cache.

        Args:
            agent_type (str): 'analyzer' or 'recommender'.
            **params: Additional parameters for agent initialization.

        Returns:
            Instance of the requested agent.
        """
        if agent_type == 'analyzer':
            return AnalyzerAgent()

        else:
            raise NotImplementedError(f"Unknown agent: {agent_type}")