# agents/supervisor/router.py
from langchain_core.messages import HumanMessage
from llms.model import LLMService
import re

llm = LLMService(prompt_type="chat")


def classify_intent(messages: list) -> str:
    """
    Classifies user intent deterministically for known commands.
    Falls back to LLM for ambiguous messages.
    Unknown defaults to 'validate'.
    """
    if not messages:
        return "validate"
    
    last_message = messages[-1]
    content = last_message.content.lower() if hasattr(last_message, 'content') else str(last_message)
    
    # Deterministic routing for known commands
    if "plan it" in content:
        return "plan"
    elif content.strip() == "new":
        return "new"
    elif content.strip() == "memories":
        return "memories"
    elif content.strip() == "clearmemory":
        return "clearmemory"
    elif content.strip() == "quit":
        return "quit"
    
    # LLM fallback for ambiguous messages
    try:
        response = llm.generate({
            "messages": messages,
            "user_input": f"Classify this message as one of: plan, validate, new, memories, clearmemory, quit. Message: {content}"
        })
        intent = response.strip().lower()
        valid_intents = ["plan", "validate", "new", "memories", "clearmemory", "quit"]
        if intent in valid_intents:
            return intent
    except Exception:
        pass
    
    # Default to validate
    return "validate"
