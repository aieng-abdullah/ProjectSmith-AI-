"""
CLI entry point for ProjectSmith-AI.

This file allows you to run the chatbot directly from the command line.
It uses the Chatbot class from chatbot/app.py and streams responses
to the terminal.
"""

from llms.model import LLMService 

import streamlit as st

def main():

    persona=input("(bp//pshycho)")
    llm = LLMService(prompt_type=persona)


    while True:

        user_input=input("user")

        print("Ai: ", end="", flush=True)
        for chunk in llm.generate(user_input):
            print(chunk, end="", flush=True)
        print() 





if __name__ == "__main__":
    main()
