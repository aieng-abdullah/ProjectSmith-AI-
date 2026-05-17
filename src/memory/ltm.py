"""
LTM — Long Term Memory via Supabase.
Handles summaries and facts for all personas.
"""

import logging
from supabase import create_client
from llms.config import settings

logger = logging.getLogger(__name__)


def _create_client():
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        logger.warning(
            "Supabase LTM disabled: SUPABASE_URL and SUPABASE_KEY are required"
        )
        return None

    try:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception:
        logger.exception("Failed to initialize Supabase client")
        return None


client = _create_client()


def init_ltm():
    if client:
        logger.info("Supabase LTM ready")
    else:
        logger.warning(
            "Supabase LTM not configured; continuing without long-term memory"
        )


# ─── SAVE ────────────────────────────────────────────────────────


def save_summary(user_id: str, persona: str, summary: str) -> bool:
    if client is None:
        logger.warning("Skipping save_summary because Supabase is not configured")
        return False

    try:
        client.table("long_term_memory").insert(
            {
                "user_id": user_id,
                "persona": persona,
                "memory_type": "summary",
                "content": summary,
            }
        ).execute()
        logger.info(f"Summary saved | user={user_id} persona={persona}")
        return True
    except Exception:
        logger.exception("save_summary failed")
        return False


def save_fact(user_id: str, persona: str, facts: str) -> bool:
    if client is None:
        logger.warning("Skipping save_fact because Supabase is not configured")
        return False

    try:
        client.table("long_term_memory").insert(
            {
                "user_id": user_id,
                "persona": persona,
                "memory_type": "fact",
                "content": facts,
            }
        ).execute()
        logger.info(f"Fact saved | user={user_id} persona={persona}")
        return True
    except Exception:
        logger.exception("save_fact failed")
        return False


# ─── LOAD ────────────────────────────────────────────────────────


def load_memories(user_id: str, persona: str) -> str:
    """Basic load — returns all memories joined as string."""
    if client is None:
        logger.warning("Skipping load_memories because Supabase is not configured")
        return ""

    try:
        result = (
            client.table("long_term_memory")
            .select("content")
            .eq("user_id", user_id)
            .eq("persona", persona)
            .order("created_at", desc=True)
            .execute()
        )
        memories = result.data
        return " | ".join([m["content"] for m in memories]) if memories else ""
    except Exception:
        logger.exception("load_memories failed")
        return ""


def supabase_load_memories(user_id: str, persona: str, limit: int = 7) -> str:
    """Load with limit — used by ltm_manager at session start."""
    if client is None:
        logger.warning(
            "Skipping supabase_load_memories because Supabase is not configured"
        )
        return ""

    try:
        result = (
            client.table("long_term_memory")
            .select("content")
            .eq("user_id", user_id)
            .eq("persona", persona)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        memories = result.data
        return " | ".join([m["content"] for m in memories]) if memories else ""
    except Exception:
        logger.exception("supabase_load_memories failed")
        return ""


# ─── ADMIN ───────────────────────────────────────────────────────


def list_memories(user_id: str) -> list:
    """Returns all raw memory rows for a user."""
    if client is None:
        logger.warning("Skipping list_memories because Supabase is not configured")
        return []

    try:
        result = (
            client.table("long_term_memory")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return result.data if result.data else []
    except Exception:
        logger.exception("list_memories failed")
        return []


def delete_memories(user_id_or_id: str) -> bool:
    """
    Delete by row ID (if numeric) or by user_id (wipes all).
    """
    if client is None:
        logger.warning("Skipping delete_memories because Supabase is not configured")
        return False

    try:
        if user_id_or_id.isdigit():
            client.table("long_term_memory").delete().eq(
                "id", int(user_id_or_id)
            ).execute()
            logger.info(f"Deleted memory row id={user_id_or_id}")
        else:
            client.table("long_term_memory").delete().eq(
                "user_id", user_id_or_id
            ).execute()
            logger.info(f"Deleted all memories for user={user_id_or_id}")
        return True
    except Exception:
        logger.exception("delete_memories failed")
        return False
