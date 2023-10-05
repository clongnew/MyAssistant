from langchain.text_splitter import RecursiveCharacterTextSplitter
from doc_load import load_url_tag_content
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from my_embedding import MyEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI


def web_scraping(url, query):
    """
    根据网页 URL 的内容回答问题 query
    """
    all_splits = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)

    div_text = load_url_tag_content(url)
    div_splits = splitter.split_text(div_text)
    div_splits = [Document(page_content=s, metadata={'source': url}) for s in div_splits]
    all_splits.extend(div_splits)
    vectorstore = Chroma.from_documents(all_splits, embedding=OpenAIEmbeddings())
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=vectorstore.as_retriever())
    res = qa_chain({"question": query})
    return res
