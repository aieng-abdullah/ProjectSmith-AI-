from langchain_community.tools import DuckDuckGoSearchRun
import logging

logger = logging.getLogger(__name__)

search = DuckDuckGoSearchRun()


def web_search(query: str) -> str:
    try:
        result = search.run(query)
        return result
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return ""


def search_pricing(idea: str) -> str:
    try:
        result = search.run(f"best free tools to build {idea} startup 2025")
        return result[:1000]  # keep it short
    except Exception as e:
        logger.error(f"Pricing search failed: {e}")
        return ""


def search_competitors(idea: str) -> str:
    try:
        result = search.run(f"existing apps similar to {idea} startup competitors")
        return result[:1000]
    except Exception as e:
        logger.error(f"Competitor search failed: {e}")
        return ""