#Purpose of the Program:
#In the following lines we run ChatGPT querry from the command line(terminal)
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import argparse

load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("--task", default="return a list of numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()

api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI()

# Prompt 1
code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"]
)

# Prompt 2
test_prompt = PromptTemplate(
    template="Write a test for {code} in this {language}",
    input_variables=["code", "language"]
)

# Chain 1
code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key="code"
)
# Chain 2
test_chain = LLMChain(
    llm=llm,
    prompt=test_prompt,
    output_key="test"
)

chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["language", "task"],
    output_variables=["test", "code"]
)

# Output 1
result = chain({
    "language" : args.language,
    "task": args.task
})
print(">>>>>>GENERATED CODE: ")
print(result["code"])
print(">>>>>>GENERATED TEST")
print(result["test"])








