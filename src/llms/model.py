import logging
from typing import Optional, List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llms.config import settings
from llms.prompts import balckpill_prompt ,engineer_prompt, psycho_prompt

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
        llm=ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            streaming=self.streaming
        )


        prompt=self.get_prompt(self.prompt_type)
        
        parser = StrOutputParser()
        return prompt | llm | parser



    def get_prompt(self, prompt_type:str):
        if prompt_type == "bp":
            return ChatPromptTemplate.from_messages([
            ("system", balckpill_prompt),
            ("human", "{input}")
        ])


        elif prompt_type == "eninner":
            return ChatPromptTemplate.from_messages([
            ("system", engineer_prompt),
            ("human", "{input}")
        ])

        elif prompt_type=="psycho":
             return ChatPromptTemplate.from_messages([
            ("system", psycho_prompt),
            ("human", "{input}")
        ])
            
        else:
            raise ValueError("invalid prompt")
        


    
    #responce genarating function
    def generate(self, user_input: str) :
        
        try:
            for chunk in self.chain.stream({"input":user_input}):
                if chunk:
                    yield chunk
                    


        except Exception as e:
            logger.exception("streaming faild...")
            yield "\n[Error: Model response interrupted.]"
        



