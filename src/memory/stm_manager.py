import logging

logger = logging.getLogger(__name__)

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