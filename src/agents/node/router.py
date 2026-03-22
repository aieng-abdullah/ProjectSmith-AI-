from agents.state import AgentState
from memory.ltm import LongTermMemory
from llms.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize LTM once
settings = settings.load()
ltm = LongTermMemory(settings.POSTGRES_URL)


def router_node(state: AgentState) -> AgentState:
    """Retrieve relevant context from long-term memory based on user input."""
    query = state['user_input']
    logger.info("Router retrieving context for query: %s", query[:50])
    
    try:
        retrieved = ltm.retrieve(query, k=3)
        state['retrieved_context'] = retrieved
        logger.info("Retrieved %d context items", len(retrieved))
    except Exception as e:
        logger.error("Failed to retrieve context: %s", str(e))
        state['retrieved_context'] = []
    
    return state
