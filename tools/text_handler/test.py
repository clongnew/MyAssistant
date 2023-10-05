# from selenium import webdriver
# from chromedriver_py import binary_path
#
# from selenium.webdriver.chrome.service import Service
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
#
# import time
# import random
#
# collection_url = 'https://www.zhihu.com/collection/512864908'
# collection_url = 'https://www.zhihu.com/collection/169110374'
# collection_url = 'https://www.zhihu.com/collection/338362696'
#
# # binary_path = '/Users/mac/Downloads/chrome-mac-x64'
# service = Service(executable_path=binary_path)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=service, options=options)
# driver.get(collection_url)
#
#
# # 等待页面加载完成
#
# def f(x):
#     href = x.get_attribute('href')
#     if href and ('answer' in href or 'zhuanlan' in href):
#         return href
#     else:
#         return None
#
#
# links = []
# while True:
#     driver.implicitly_wait(10)
#
#     page_links = driver.find_elements(By.CSS_SELECTOR, 'a')
#     print('原始 page_links: ', page_links, '\n')
#     page_links = [f(x) for x in page_links if f(x)]
#     #     page_links = driver.execute_script("""
#     #         return Array.from(document.querySelectorAll('a'))
#     #             .map(a => a.href)
#     #             .filter(href => href.includes('answer') || href.includes('zhuanlan'))
#     #     """)
#     print(page_links, '---\n')
#     links += page_links
#
#     wait = WebDriverWait(driver, 10)
#     next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.PaginationButton-next')))
#
#     driver.implicitly_wait(10)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     # 检查是否找到下一页按钮，如果没有就退出循环
#     if not next_button:
#         break
#     print(next_button)
#     # 模拟鼠标点击下一页按钮
#     time.sleep(3 + random.random())
#     actions = ActionChains(driver)
#     actions.move_to_element(next_button).click().perform()
#     driver.implicitly_wait(10)
#
# #     next_button.click()
# driver.quit()
# print('-----length-----: {}'.format(len(links)))

from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer

# 1 利用 serper 获取网页信息
# 2 extract 获取分段信息，所有分段信息+snippet，以 serper 标题为title并加入 vectorstore chroma.from_documents
# 3 将 vectorstore 作为 retriever 用 sourceqa 来做最后的回答

import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
print(f'parent_dir: {parent_dir}')
sys.path.append(parent_dir)

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ["OPENAI_API_KEY"] = 'fk200821-RPW7NmOKUwdGFU7w6aaN54hyn2OkUKYt'
os.environ['OPENAI_API_BASE'] = 'https://oa.api2d.net/v1'
os.environ["SERPER_API_KEY"] = "d85bb10b73cb5bf80372a6218e59471ffe53d3e6"

from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain



import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.chains import LLMChain
from doc_split import split_paragraph

from langchain.text_splitter import RecursiveCharacterTextSplitter
from doc_load import load_url_tag_content
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from my_embedding import MyEmbeddings
# from easy_functions import tagging_text
from langchain.chains import RetrievalQAWithSourcesChain
from easy_functions import tool_search_online, search1

# 总体框架
def advance_search(query):
    all_splits = []
    search_result = tool_search_online(query, k=2)['organic']
    print(type(search_result), '\n', search_result)

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)

    for each_result in search_result:
        link = each_result['link']
        title = each_result['title']
        div_text = load_url_tag_content(link)
        div_splits = splitter.split_text(div_text)
        div_splits.append(each_result['snippet'])
        div_splits = [Document(page_content=s, metadata={'source': link+'/'+title}) for s in div_splits]
        all_splits.extend(div_splits)
    vectorstore = Chroma.from_documents(all_splits, embedding=OpenAIEmbeddings())
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=vectorstore.as_retriever())
    res = qa_chain({"question": query})
    print('res:', '\n', res)
    return res

q = "langchain web scrap code"

advance_search(q)
search_result = search1(q)
print('sr:', search_result)
# @set_aboard_config
# def new_search(question):
#     # Vectorstore
#
#     embeddings_model = OpenAIEmbeddings()
#     embedding_size = 1536
#     index = faiss.IndexFlatL2(embedding_size)
#     vectorstore_public = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
#
#     # LLM
#     from langchain.chat_models import ChatOpenAI
#     llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, streaming=True)
#
#     # Search
#     from langchain.utilities import GoogleSearchAPIWrapper
#     search = GoogleSerperAPIWrapper()
#
#     # Initialize
#     web_retriever = MyRetriever.from_llm(
#         vectorstore=vectorstore_public,
#         llm=llm,
#         search=search,
#         num_search_results=3
#     )
#     qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=web_retriever)
#     result = qa_chain({"question": question})
#     return result


def summarize(url):
    # Define prompt
    prompt_template = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text"
    )
    text = clean_html(url)
    docs = split_paragraph(text)
    print('stuff_chain:', stuff_chain.run(docs))


def extract_key_info(url):
    text = clean_html(url)
    # Schema
    schema = {
        "properties": {
            "title": {"type": "string"},
            "content_summary": {"type": "string"},
            # "example_code": {"type": "string", "default": ""},
        },
        "required": ["title", "content_summary"],
    }

    # Run chain
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
    chain = create_extraction_chain(schema, llm)
    res = chain.run(text)
    print(res)
    return res[0]


def clean_html(url):
    # 发送请求，获取文章内容
    res = {}
    response = requests.get(url)
    content = response.text

    # 去除HTML标签，只保留纯文本
    soup = BeautifulSoup(content, 'html.parser')
    valid_tags = ['div', 'span']
    for tag in valid_tags:
        soup_tag = soup.find_all(tag)
        lis_tag = [t.get_text(strip=True) for t in soup_tag if len(tt := t.get_text(strip=True)) > 10]

        res[tag] = list(set(lis_tag))
    prompt = "以下是一个网页的html内容：\n"
    for tag in res:
        prompt += tag + ": \n\n" + "\n".join(res[tag]) + "\n\n"
    print(f'prompt: {prompt}')
    return prompt



url = 'https://medium.com/@onkarmishra/using-langchain-for-question-answering-on-own-data-3af0a82789ed'
url = 'https://zhuanlan.zhihu.com/p/644671690'
# summarize(url)
# clean_html(url)


# f1('https://medium.com/@onkarmishra/using-langchain-for-question-answering-on-own-data-3af0a82789ed')
