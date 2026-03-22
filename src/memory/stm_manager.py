"""
STM utilities — trim, summarize.
Trim runs automatically on every LLM call.
Summarize is called manually via 'summarize' command in CLI.
"""

import logging 
from langchain_core.messages import AIMessage , HumanMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llms.model import LLMService

logger = logging.getLogger(__name__)

Max_Token = 500


_llm=LLMService(prompt_type="bp",streaming=False).llm



#Triming messages

def trim(messages: list) -> list:
    """
    Filters messages to MAX_TOKENS before passing to LLM.
    Uses simple word-based counting — good enough for prototyping.
    """
    if not messages:
        return []

    try:
        # simple token counter — no extra dependencies needed
        # roughly 1 token per 4 characters
        def count_tokens(msgs):
            return sum(len(str(m.content)) // 4 for m in msgs)

        return trim_messages(
            messages,
            token_counter=count_tokens,  # simple counter, no transformers needed
            max_tokens=Max_Token,
            strategy="last",
            include_system=True,
            allow_partial=False,
        )
    except Exception as e:
        logger.exception("trim failed returning original")
        return messages
    
    
