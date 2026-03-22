"""
CRUD operations for short term memory.
Queries the checkpoints table that LangGraph creates automatically.
No custom table needed — LangGraph manages storage.
"""
import logging
import psycopg
from llms.config import settings

logger = logging.getLogger(__name__)


def _connect():
    """Single reusable connection."""
    return psycopg.connect(settings.POSTGRES_URL, autocommit=True)



def get_thread(thread_id: str) -> dict | None:
    """
    Get the latest checkpoint for a thread.
    Returns full state dict or None if not found.
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT checkpoint_id,
                           checkpoint,
                           metadata
                    FROM checkpoints
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id DESC
                    LIMIT 1
                """, (thread_id,))

                row = cur.fetchone()
                if not row:
                    logger.info(f"No checkpoint found: {thread_id}")
                    return None

                return {
                    "thread_id":     thread_id,
                    "checkpoint_id": row[0],
                    "checkpoint":    row[1],
                    "metadata":      row[2],
                }

    except Exception as e:
        logger.exception(f"get_thread failed: {thread_id}")
        return None


def get_messages(thread_id: str) -> list:
    """
    Get just the messages from the latest checkpoint.
    Returns list of message dicts or empty list.
    """
    try:
        thread = get_thread(thread_id)
        if not thread:
            return []

        messages = (
            thread["checkpoint"]
            .get("channel_values", {})
            .get("messages", [])
        )

        logger.info(f"Found {len(messages)} messages for thread: {thread_id}")
        return messages

    except Exception as e:
        logger.exception(f"get_messages failed: {thread_id}")
        return []


def list_threads(user_id: str) -> list[dict]:
    """
    List all threads for a specific user.
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT ON (thread_id)
                        thread_id,
                        checkpoint_id,
                        metadata
                    FROM checkpoints
                    WHERE metadata->>'user_id' = %s
                    ORDER BY thread_id, checkpoint_id DESC
                """, (user_id,))

                rows = cur.fetchall()

                if not rows:
                    logger.info(f"No threads found for user: {user_id}")
                    return []

                return [
                    {
                        "thread_id":     row[0],
                        "checkpoint_id": row[1],
                        "metadata":      row[2],
                    }
                    for row in rows
                ]

    except Exception as e:
        logger.exception(f"list_threads failed: {user_id}")
        return []


def list_all_threads() -> list[str]:
    """
    List every thread_id in the database.
    Useful for debugging.
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT thread_id
                    FROM checkpoints
                    ORDER BY thread_id
                """)
                rows = cur.fetchall()
                return [row[0] for row in rows]

    except Exception as e:
        logger.exception("list_all_threads failed")
        return []


# ─── DELETE ──────────────────────────────────────────────────────

def delete_thread(thread_id: str) -> bool:
    """
    Delete all checkpoints for one thread.
    Permanent — cannot be undone.
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM checkpoints
                    WHERE thread_id = %s
                """, (thread_id,))

                deleted = cur.rowcount
                logger.info(f"Deleted {deleted} rows for thread: {thread_id}")
                return True

    except Exception as e:
        logger.exception(f"delete_thread failed: {thread_id}")
        return False


def delete_all_threads(user_id: str) -> bool:
    """
    Delete ALL threads for a user.
    Permanent — cannot be undone.
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM checkpoints
                    WHERE metadata->>'user_id' = %s
                """, (user_id,))

                deleted = cur.rowcount
                logger.info(f"Deleted {deleted} rows for user: {user_id}")
                return True

    except Exception as e:
        logger.exception(f"delete_all_threads failed: {user_id}")
        return False