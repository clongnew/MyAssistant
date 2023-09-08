from langchain.vectorstores import Chroma
from .my_embedding import MyEmbeddings


# 持久化向量数据
def persist_embedding(documents, persist_directory):
    # 将embedding数据持久化到本地磁盘
    embedding = MyEmbeddings()
    # embedding = HuggingFaceEmbeddings()
    # embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=documents, embedding=embedding, persist_directory=persist_directory)
    vectordb.persist()
    vectordb = None

def add_embedding(documents, persist_directory):
    embedding = MyEmbeddings()
    # embedding = HuggingFaceEmbeddings()
    # embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    vectordb.add_documents(documents=documents)
    vectordb.persist()
    vectordb = None

def load_embedding(persist_directory):
    embedding = MyEmbeddings()
    # embedding = HuggingFaceEmbeddings()
    # embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    return retriever