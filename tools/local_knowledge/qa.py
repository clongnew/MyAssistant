from my_embedding import MyEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import yaml
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir, 'config.yaml')
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)
persist_directory = config['persist_directory']
global retriever

def load_embedding():
    embedding = MyEmbeddings()
    # embedding = HuggingFaceEmbeddings()
    # embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})


def answer(query):
    prompt_template = """请注意：请谨慎评估query与提示的Context信息的相关性，只根据本段输入文字信息的内容进行回答，如果query与提供的材料无关，请回答"我不知道"，另外也不要回答无关答案：
    Context: {context}
    Context: {context}
    Question: {question}
    Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    docs = retriever.get_relevant_documents(query)

    # 基于docs来prompt，返回你想要的内容
    chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff", prompt=PROMPT)
    result = chain({"input_documents": docs, "question": query}, return_only_outputs=False)
    return result


if __name__ == "__main__":
    # load embedding
    load_embedding()
    # 循环输入查询，直到输入 "exit"
    while True:
        query = input("Enter query (or 'exit' to quit): ")
        if query == 'exit':
            print('exit')
            break
        print("Query:" + query + '\nAnswer:\n')
        print(answer(query), '\n')

from langchain.chains import RetrievalQA

from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

link = 'https://zhuanlan.zhihu.com/p/641132245'
text = load_url_content(link)
documents = split_paragraph(text, file_name=link)
embeddings = OpenAIEmbeddings()
# create the vectorestore to use as the index
db = Chroma.from_documents(documents=documents, embedding=embeddings)
# expose this index in a retriever interface
retriever = db.as_retriever(search_kwargs={"k":5})
# 提示词
prompt_template = """请注意：请谨慎评估query与提示的Context信息的相关性，
    然后根据本段输入文字信息的内容并结合你的知识进行回答，如果你的知识和材料信息都无法解答query，请回答"我的本地知识无法解决这个问题"，另外也不要回答无关答案：
    Context: {context}
    Context: {context}
    Question: {question}
    Answer:"""
prompt_lk = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
# create a chain to answer questions
chain_type_kwargs = {'prompt': prompt_lk}
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name='gpt-3.5-turbo'), chain_type="stuff",
    retriever=retriever, chain_type_kwargs=chain_type_kwargs)

