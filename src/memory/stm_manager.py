import logging
from langchain_core.messages import trim_messages

logger = logging.getLogger(__name__)

MAX_TOKENS = 500

def trim(messages: list) -> list:
    if not messages:
        return []
    try:
        def count_tokens(msgs):
            return sum(len(str(m.content)) // 4 for m in msgs)
        return trim_messages(
            messages,
            token_counter=count_tokens,
            max_tokens=MAX_TOKENS,
            strategy="last",
            include_system=True,
            allow_partial=False,
        )
    except Exception as e:
        logger.exception("trim failed, returning original")
        return messages

def get_thread(thread_id: str) -> dict | None:
    return None

def get_messages(thread_id: str) -> list:
    return []

def list_threads(user_id: str) -> list[dict]:
    return []

def list_all_threads() -> list[str]:
    return []

def delete_thread(thread_id: str) -> bool:
    return True

def delete_all_threads(user_id: str) -> bool:
    return True