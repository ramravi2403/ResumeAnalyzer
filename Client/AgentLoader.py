from Server import AnalyzerAgent, RecommendationAgent
from streamlit import cache_resource

class AgentLoader:

    _default_course_file = "./Server/downsized_dataset.csv"

    @classmethod
    @cache_resource
    def load(cls, agent_type: str, data_file: str = _default_course_file):
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
        elif agent_type == 'recommender':
            return RecommendationAgent(course_data_file=data_file)
        else:
            raise NotImplementedError(f"Unknown agent: {agent_type}")
