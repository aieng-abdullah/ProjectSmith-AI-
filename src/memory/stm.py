import logging
import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from llms.config import settings

logger = logging.getLogger(__name__)


def get_checkpointer() -> PostgresSaver:
    try:
        # open connection manually — don't use 'with' so it stays open
        conn = psycopg.connect(settings.POSTGRES_URL, autocommit=True)
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()

        logger.info("Short term memory ready")
        return checkpointer

    except Exception as e:
        logger.exception("Short term memory connection failed")
        raise RuntimeError(
            f"Could not connect to Postgres. Is Docker running?\nError: {e}"
        )


checkpointer = get_checkpointer()