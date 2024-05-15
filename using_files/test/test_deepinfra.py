import os

from langchain.memory import ConversationBufferWindowMemory

from chatAll import config
from langchain_community.llms import DeepInfra
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

llm = DeepInfra(model_id=config.LLM_MODEL_NAME)
llm.model_kwargs = {
    "temperature": 0.7,
    "top_p": 0.9,
}
# print(llm.invoke("HELLO?"))

template = """Given the following user prompt and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.
  You should follow the following rules when generating and answer:
  - Always prioritize the user prompt over the conversation log.
  - Ignore any conversation log that is not directly related to the user prompt.
  - Only attempt to answer if a question was posed.
  - The question should be a single sentence.
  - You should remove any punctuation from the question.
  - You should remove any words that are not relevant to the question.
  - If you are unable to formulate a question, respond with the same USER PROMPT you got.
 
Conversation log: {history}
USER PROMPT: {question}
"""
prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)

llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True,
                     memory=ConversationBufferWindowMemory(k=10), )

question = "我应该如何学习langchain?"
response = llm_chain.invoke(question)

print(response)
