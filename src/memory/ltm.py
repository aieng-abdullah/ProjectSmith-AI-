import logging
import psycopg
from llms.config import settings

logger = logging.getLogger(__name__)

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS long_term_memory (
    id          SERIAL PRIMARY KEY,
    user_id     TEXT        NOT NULL,
    persona     TEXT        NOT NULL,
    memory_type TEXT        NOT NULL,
    content     TEXT        NOT NULL,
    created_at  TIMESTAMP   DEFAULT NOW()
);
"""

CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS ltm_user_id_idx
ON long_term_memory (user_id, persona);
"""


def _connect():
    return psycopg.connect(settings.POSTGRES_URL, autocommit=True)


def init_ltm():
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE)
                cur.execute(CREATE_INDEX)
        logger.info("LTM table ready")
    except Exception as e:
        logger.exception("LTM init failed")
        raise RuntimeError(f"LTM init failed: {e}")


def save_summary(user_id: str, persona: str, summary: str) -> bool:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO long_term_memory
                        (user_id, persona, memory_type, content)
                    VALUES (%s, %s, 'summary', %s)
                """, (user_id, persona, summary))
        logger.info(f"Summary saved for user: {user_id}")
        return True
    except Exception as e:
        logger.exception("save_summary failed")
        return False


def save_fact(user_id: str, persona: str, fact: str) -> bool:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO long_term_memory
                        (user_id, persona, memory_type, content)
                    VALUES (%s, %s, 'fact', %s)
                """, (user_id, persona, fact))
        logger.info(f"Fact saved for user: {user_id}")
        return True
    except Exception as e:
        logger.exception("save_fact failed")
        return False


def fetch_memories(user_id: str, persona: str, limit: int = 5) -> str:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT memory_type, content, created_at
                    FROM long_term_memory
                    WHERE user_id = %s AND persona = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (user_id, persona, limit))
                rows = cur.fetchall()

        if not rows:
            return ""

        lines = ["[What you know about this user from past sessions:]"]
        for memory_type, content, created_at in reversed(rows):
            date = created_at.strftime("%Y-%m-%d")
            lines.append(f"[{date} | {memory_type}]: {content}")

        return "\n".join(lines)

    except Exception as e:
        logger.exception("fetch_memories failed")
        return ""


def delete_memories(user_id: str) -> bool:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM long_term_memory
                    WHERE user_id = %s
                """, (user_id,))
                deleted = cur.rowcount
                logger.info(f"Deleted {deleted} memories for user: {user_id}")
                return True
    except Exception as e:
        logger.exception("delete_memories failed")
        return False


def list_memories(user_id: str) -> list[dict]:
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, memory_type, content, created_at
                    FROM long_term_memory
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
                rows = cur.fetchall()
                return [
                    {
                        "id":         row[0],
                        "type":       row[1],
                        "content":    row[2],
                        "created_at": row[3].strftime("%Y-%m-%d %H:%M"),
                    }
                    for row in rows
                ]
    except Exception as e:
        logger.exception("list_memories failed")
        return []