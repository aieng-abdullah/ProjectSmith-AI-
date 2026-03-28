"""
LTM Manager — summarize, extract facts, load memories.
Called by main.py on session start and end.
"""
import logging
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from memory.ltm import save_summary, save_fact, fetch_memories
from llms.model import LLMService

logger = logging.getLogger(__name__)

# reuse LLM from LLMService — no new instance
_llm = LLMService(prompt_type="advisor", streaming=False).llm


# ─── SUMMARIZE AND SAVE ──────────────────────────────────────────

def summarize_and_save(
    messages: list,
    user_id: str,
    persona: str
) -> bool:
    """
    Summarizes conversation and saves to LTM.
    Called at end of session — on quit or new.
    """
    if not messages:
        return False

    transcript = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            transcript.append(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            transcript.append(f"Assistant: {msg.content}")

    transcript_text = "\n".join(transcript)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You summarize therapy conversations clearly and concisely."),
        ("human", """Summarize this conversation in 3-5 sentences.
Focus on: key topics, user emotional state, important facts mentioned.
This summary will be injected into future sessions as memory context.

Conversation:
{transcript}

Summary:""")
    ])

    chain = prompt | _llm | StrOutputParser()

    try:
        summary = chain.invoke({"transcript": transcript_text})
        saved   = save_summary(user_id, persona, summary)
        logger.info(f"Summary saved for user: {user_id}")
        return saved
    except Exception as e:
        logger.exception("summarize_and_save failed")
        return False


# ─── EXTRACT AND SAVE FACTS ──────────────────────────────────────

def extract_and_save_facts(
    messages: list,
    user_id: str,
    persona: str
) -> bool:
    """
    Extracts key facts about the user from last 5 messages.
    Called automatically every 5 messages during conversation.
    """
    if not messages:
        return False

    # only look at last 5 messages
    recent = messages[-5:]

    transcript = []
    for msg in recent:
        if isinstance(msg, HumanMessage):
            transcript.append(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            transcript.append(f"Assistant: {msg.content}")

    transcript_text = "\n".join(transcript)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You extract key facts about users from conversations."),
        ("human", """Extract key facts about the user from this conversation.
Focus on: name, age, location, occupation, emotional state, life events, goals.
Write as short bullet points.
If no clear facts found, return exactly: 'no facts found'

Conversation:
{transcript}

Facts:""")
    ])

    chain = prompt | _llm | StrOutputParser()

    try:
        facts = chain.invoke({"transcript": transcript_text})

        if "no facts found" in facts.lower():
            logger.info("No facts extracted")
            return False

        saved = save_fact(user_id, persona, facts)
        logger.info(f"Facts saved for user: {user_id}")
        return saved

    except Exception as e:
        logger.exception("extract_and_save_facts failed")
        return False


# ─── LOAD MEMORIES ───────────────────────────────────────────────

def load_memories(user_id: str, persona: str) -> str:
    """
    Fetches LTM for this user.
    Called at session start — result injected into system prompt.
    Returns empty string if no memories found.
    """
    memories = fetch_memories(user_id, persona, limit=5)

    if not memories:
        logger.info(f"No LTM found for user: {user_id}")
        return ""

    logger.info(f"LTM loaded for user: {user_id}")
    return memories