# 放置简单函数
import os
from langchain import SerpAPIWrapper
from langchain import GoogleSerperAPIWrapper
import yaml
import functools
import subprocess
import time

# 设置全局变量，供需要访问外网的工具
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
refer_dir = os.path.join(os.path.join(parent_dir, 'assist_refer_files'))
config_file = os.path.join(current_dir, 'aboard_config.yaml')

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)


def set_aboard_config(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for k, v in config.items():
            os.environ[k] = v
        result = func(*args, **kwargs)
        for k in config:
            os.environ.pop(k)
        return result

    # wrapper.__doc__ = func.__doc__
    return wrapper


@set_aboard_config
def tool_search_online(query, k=3):
    """当你遇到不确定的知识或者 human 希望你基于网络信息回答时，你可以使用它查询网上相关知识；
    在需要查询实时信息时，你可以优先使用这个工具；
    你也可以使用它帮助你完善你的回答
    """
    search = GoogleSerperAPIWrapper()
    search.k = k
    return search.run(query=query)


@set_aboard_config
def search_userful_urls(query, k=5):
    """
    查询一些关键的网页 URL 以便进一步分析
    """
    search = GoogleSerperAPIWrapper()
    search.k = k
    res = search.results(query=query)['organic']
    return [r['link'] for r in res]


def run_code(code: str, log_path=''):
    """
    目的：
    你可以利用它执行代码。

    :params
    code: 需要执行的代码
    log_path: 代码文件和日志文件的存储位置

    :return
    它将为你返回代码执行结果或者报错。如果返回报错，请尝试修改代码并重新执行。
    """
    if log_path == '':
        current_timestamp = int(time.time())
        timestamp_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(current_timestamp))
        log_path = os.path.join(refer_dir, timestamp_str)
        os.makedirs(log_path, exist_ok=True)
    temp_script = os.path.join(log_path, 'temp_script.py')
    with open(temp_script, "w") as temp_file:
        temp_file.write(code)
    try:
        # Execute the script and capture the output
        result = subprocess.run(['/usr/local/lib/python3/ci/bin/python', temp_script],
                                capture_output=True, text=True, check=True)
        return {'代码执行结果': result.stdout}
    except subprocess.CalledProcessError as e:
        # Handle execution errors
        error_path = os.path.join(log_path, 'ci_error')
        with open(error_path, 'w') as error_file:
            error_file.write(repr(e) + '\n' + e.stderr)
        return {'代码出错了，请根据报错尝试更正代码': e.stderr}
    # finally:
    #     # Clean up the temporary script file
    #     subprocess.run(["rm", temp_script])


# 所有待输出的工具函数
easy_funcs = [tool_search_online, run_code, search_userful_urls]
