import PyPDF2
import requests
from bs4 import BeautifulSoup

# 加载PDF文件
def load_pdf(pdf_file):
    pdf_file = open(pdf_file, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ''
    for num in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[num]
      text += page.extract_text()
    return text

# 读取 txt 文件，并转为字符串
def load_txt(txt_file):
    with open(txt_file, 'r') as file:
        text = file.read()
    return text

# 读取博客
def load_url_content(url):
    # 发送请求，获取文章内容
    response = requests.get(url)
    content = response.text

    # 去除HTML标签，只保留纯文本
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()

    return text

    