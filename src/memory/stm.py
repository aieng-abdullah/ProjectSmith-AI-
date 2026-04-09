import logging
from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)

def get_checkpointer():
    checkpointer = MemorySaver()
    logger.info("Short term memory ready (in-memory)")
    return checkpointer

checkpointer = get_checkpointer()