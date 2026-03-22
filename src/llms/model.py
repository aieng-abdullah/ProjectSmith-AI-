"""

LLM Service Module



This module provides a service layer for interacting with Groq-hosted

language models through LangChain. It handles:



- Prompt selection

- LLM initialization

- Response streaming

- Output parsing



The service builds a LangChain pipeline composed of:

PromptTemplate -> LLM -> OutputParser

"""









import logging

from typing import Optional, List

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

from llms.config import settings

from llms.prompts import balckpill_prompt ,engineer_prompt, psycho_prompt
from agents.state import AgentState
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



logger = logging.getLogger(__name__)





class LLMService:

    """

    Docstring for LLMServic

    """



    def __init__(

        self,

        prompt_type:str,

        streaming: bool = True,

        callbacks: Optional[List] = None,

        ):

        



        self.prompt_type = prompt_type

        self.streaming=streaming

        self.callbacks =callbacks or []

        self.chain =self.build_chain()

        







    def build_chain(self):

        self.llm=ChatGroq(

            groq_api_key=settings.GROQ_API_KEY,

            model_name=settings.MODEL_NAME,

            temperature=settings.TEMPERATURE,

            streaming=self.streaming

        )
        





        prompt=self.get_prompt(self.prompt_type)

        

        parser = StrOutputParser()

        return prompt | self.llm | parser







    def get_prompt(self, prompt_type: str):
        templates = {
        "bp":       balckpill_prompt,
        "engineer": engineer_prompt,
        "psycho":   psycho_prompt,
         }

        if prompt_type not in templates:
            raise ValueError(f"Invalid prompt type: '{prompt_type}'")

        return ChatPromptTemplate.from_messages([
        ("system", templates[prompt_type] + "\n\n{ltm_context}"),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
         ])
 

    #responce genarating function

    def generate(self, state: AgentState):
        try:
            ltm = state.get("ltm_context", "")
            

            payload = {
                "input":       state["user_input"],
                "messages":    state.get("messages", []),
                "ltm_context": ltm,
            }

            for chunk in self.chain.stream(payload):
                if chunk:
                    yield chunk

        except KeyError as e:
            logger.error(f"Missing key in state: {e}")
            yield f"\n[Error: Missing state key {e}]"

        except Exception as e:
            logger.exception("Streaming failed")
            yield "\n[Error: Model response interrupted.]"