"""
LTM — Long Term Memory via Supabase.
Handles summaries and facts for all personas.
"""
import logging
from supabase import create_client
from llms.config import settings

logger = logging.getLogger(__name__)

client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def init_ltm():
    logger.info("Supabase LTM ready")


# ─── SAVE ────────────────────────────────────────────────────────

def save_summary(user_id: str, persona: str, summary: str) -> bool:
    try:
        client.table('long_term_memory').insert({
            'user_id':      user_id,
            'persona':      persona,
            'memory_type':  'summary',
            'content':      summary
        }).execute()
        logger.info(f"Summary saved | user={user_id} persona={persona}")
        return True
    except Exception as e:
        logger.exception("save_summary failed")
        return False


def save_fact(user_id: str, persona: str, facts: str) -> bool:
    try:
        client.table('long_term_memory').insert({
            'user_id':      user_id,
            'persona':      persona,
            'memory_type':  'fact',
            'content':      facts
        }).execute()
        logger.info(f"Fact saved | user={user_id} persona={persona}")
        return True
    except Exception as e:
        logger.exception("save_fact failed")
        return False


# ─── LOAD ────────────────────────────────────────────────────────

def load_memories(user_id: str, persona: str) -> str:
    """Basic load — returns all memories joined as string."""
    try:
        result = (
            client.table('long_term_memory')
            .select('content')
            .eq('user_id', user_id)
            .eq('persona', persona)
            .order('created_at', desc=True)
            .execute()
        )
        memories = result.data
        return " | ".join([m['content'] for m in memories]) if memories else ""
    except Exception as e:
        logger.exception("load_memories failed")
        return ""


def supabase_load_memories(user_id: str, persona: str, limit: int = 7) -> str:
    """Load with limit — used by ltm_manager at session start."""
    try:
        result = (
            client.table('long_term_memory')
            .select('content')
            .eq('user_id', user_id)
            .eq('persona', persona)
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        memories = result.data
        return " | ".join([m['content'] for m in memories]) if memories else ""
    except Exception as e:
        logger.exception("supabase_load_memories failed")
        return ""


# ─── ADMIN ───────────────────────────────────────────────────────

def list_memories(user_id: str) -> list:
    """Returns all raw memory rows for a user."""
    try:
        result = (
            client.table('long_term_memory')
            .select('*')
            .eq('user_id', user_id)
            .order('created_at', desc=True)
            .execute()
        )
        return result.data if result.data else []
    except Exception as e:
        logger.exception("list_memories failed")
        return []


def delete_memories(user_id_or_id: str) -> bool:
    """
    Delete by row ID (if numeric) or by user_id (wipes all).
    """
    try:
        if user_id_or_id.isdigit():
            client.table('long_term_memory').delete().eq('id', int(user_id_or_id)).execute()
            logger.info(f"Deleted memory row id={user_id_or_id}")
        else:
            client.table('long_term_memory').delete().eq('user_id', user_id_or_id).execute()
            logger.info(f"Deleted all memories for user={user_id_or_id}")
        return True
    except Exception as e:
        logger.exception("delete_memories failed")
        return False