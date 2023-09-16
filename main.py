import os

# 现在不走代理，用 api2d 来访问，避免代理很多麻烦。对于需要访问外网的工具，在其中设置外网的相关设置，使用完 pop
# os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "b5212168ec2f9ec004716b620913db3bc727380839ea8e95f35938e8359ddc6e"
os.environ['PYTHONIOENCODING'] = 'utf-8'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['all_proxy'] = 'socks5://127.0.0.1:7890'
os.environ["OPENAI_API_KEY"] = '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'
os.environ['OPENAI_API_BASE'] = 'https://oa.api2d.net/v1'

from main_gradio import main_interface
from main_functions import load_history_memory, save_threading

dialogue_dic = load_history_memory()

if __name__ == '__main__':
    main_interface(dialogue_dic)
    save_threading(dialogue_dic)
