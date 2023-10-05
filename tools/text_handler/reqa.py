from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from .store_emb import load_embedding
import yaml
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir, 'config.yaml')

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

persist_directory = config['persist_directory']
retriever = load_embedding(persist_directory)

# 提示词
prompt_template = """请注意：请谨慎评估query与提示的Context信息的相关性，
    然后根据本段输入文字信息的内容并结合你的知识进行回答，如果你的知识和材料信息都无法解答query，请回答"本地知识无法解决这个问题"，另外也不要回答无关答案：
    Context: {context}
    Context: {context}
    Question: {question}
    Answer:"""
prompt_lk = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
# create a chain to answer questions
chain_type_kwargs = {'prompt': prompt_lk}
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(model_name='gpt-3.5-turbo'), chain_type="stuff",
                                              retriever=retriever, combine_docs_chain_kwargs=chain_type_kwargs,
                                              memory=memory)


def get_local_knowledge(query):
    """当你遇到不确定的知识或者 human 希望你基于本地知识回答时，你可以使用它查询本地相关知识。
    注意：请将整个 human 提供的问题主体作为输入，而不是将你总结的query中的主要参数输入这个工具。
    如果你已经输入了 query 的主要参数并得到返回答案，请仅仅将它作为一个参考，之后重新调用 get_local_knowledge 这个工具，将 human 的问题主体作为输入，并返回得到答案
    """
    return {'本地知识回答': chain({'question': query})['answer']}
