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
