import os
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service
from store_emb import persist_embedding, add_embedding
from doc_split import split_paragraph
from doc_load import load_url_content
import yaml
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir, 'config.yaml')

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

collection_url = config['collection_url']
persist_directory = config['persist_directory']
links_doc = 'links.txt'
persist_directory = os.path.join(current_dir, persist_directory)
links_doc = os.path.join(current_dir, links_doc)
os.makedirs(persist_directory, exist_ok=True)


# 1. 加载知乎收藏夹下最新的所有的 URL
def get_zhihu_collection_links(collection_id):
    api_url = f'https://www.zhihu.com/api/v4/collections/{collection_id}/items'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        # 替换为合适的 User Agent
    }
    params = {
        'offset': 0,
        'limit': 16  # 每次获取的条目数
    }
    links = []
    while True:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                items = data['data']
                if not items:
                    break
                for item in items:
                    if 'content' in item and 'url' in item['content']:
                        links.append(item['content']['url'])
                params['offset'] += params['limit']
            else:
                break
        else:
            print("Failed to fetch API data")
            break
    return links


# 指定知乎收藏夹 ID
ids = config['collection_ids'].split(',')  # 从收藏夹 URL 中获取 ID

# 获取收藏夹链接
links = []
for collection_id in ids:
    print('cid: ', collection_id)
    links += get_zhihu_collection_links(collection_id)

# 2. 查看是否有新增链接
new_links = []
if os.path.exists(links_doc):
    with open(links_doc, 'r') as f:
        old_links = f.readlines()
    old_links = [l.strip() for l in old_links]
    new_links = list(set(links) - set(old_links))
else:
    new_links = links
print('new_links: ', new_links)

# 3. 本地永久化embedding
totals = []
for link in new_links:
    try:
        text = load_url_content(link)
        documents = split_paragraph(text, file_name=link)
        totals.extend(documents)
    except Exception as e:
        with open('error.log' 'w') as f:
            f.write(f"Error while persisting embedding for link {link}: {str(e)}\n")
print('total_length: ', len(totals))
if not os.listdir(persist_directory):
    persist_embedding(totals, persist_directory=persist_directory)
else:
    add_embedding(totals, persist_directory=persist_directory)

with open(links_doc, 'a') as f:
    f.write('\n'.join(new_links))
