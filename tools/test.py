# import os
#
# # 获取当前脚本所在目录的父目录路径
# current_directory = os.path.dirname(os.path.abspath(__file__))
# parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
# print(current_directory, parent_directory)
#
# # 新文件夹的名称
# new_folder_name = "assist_refer_files"
#
# # 创建新文件夹的完整路径
# new_folder_path = os.path.join(parent_directory, new_folder_name)
#
# os.makedirs(new_folder_path, exist_ok=True)

import os

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ["OPENAI_API_KEY"] = 'fk200821-RPW7NmOKUwdGFU7w6aaN54hyn2OkUKYt'
os.environ['OPENAI_API_BASE'] = 'https://oa.api2d.net/v1'
os.environ["SERPAPI_API_KEY"] = "b5212168ec2f9ec004716b620913db3bc727380839ea8e95f35938e8359ddc6e"
os.environ["SERPER_API_KEY"] = "d85bb10b73cb5bf80372a6218e59471ffe53d3e6"
os.environ["GOOGLE_API_KEY"] = "d85bb10b73cb5bf80372a6218e59471ffe53d3e6"
os.environ["GOOGLE_CSE_ID"] = "YOUR_CSE_ID"

from easy_functions import set_aboard_config
import requests
import json
import certifi


@set_aboard_config
def f():
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": "langchain search web"
    })
    headers = {
        'X-API-KEY': 'd85bb10b73cb5bf80372a6218e59471ffe53d3e6',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=certifi.where())

    print(response.text, '\n')
