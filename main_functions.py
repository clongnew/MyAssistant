# 将主函数尽可能简化，就是保存一个 gradio 的界面加载器
import json

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from tools import tool_list
from prompts import str_main_agent_prompt
from tool_agent import create_agent, tool_agent_list
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
import os
import time
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))


# 主 agent
def create_main_agent(**kwargs):
    return create_agent(sys_message=str_main_agent_prompt,
                        mytools=tool_list + tool_agent_list, **kwargs)


# 历史记录的保存和加载
summarize_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", streaming=True)
name_dic_file = os.path.join(current_dir, 'history.json')


# 主函数中设置一个 global current_name=None，当点击提交没有名字时，调用它生成 current_name
def generate_name(text):
    prompt = f'请用一句简介的话总结以下内容： {text} \n 注意不要超过20个字符'
    return summarize_llm.predict(prompt)


# 改成 uuid
def check_name(name, name_dic):
    i = 0
    original_name = name
    while name in name_dic:
        i += 1
        name = original_name + f'_{i}'
    return name


# 每点击一次提交，就更新一次 key: current_dialogue
def m2j(m):
    j = m.chat_memory.messages
    return messages_to_dict(j)


def save_history_json(name_dic):
    json_dic = {k: m2j(v) for k, v in name_dic.items()}
    with open(name_dic_file, 'w') as file:
        json.dump(json_dic, file, indent=4)


def load_history_memory():
    try:
        with open(name_dic_file, 'r') as file:
            dic = json.load(file)
    except:
        return {}
    memory_dic = {}
    for k, v in dic.items():
        retrieved_messages = messages_from_dict(v)
        retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)
        retrieved_memory = ConversationBufferMemory(chat_memory=retrieved_chat_history,
                                                    memory_key='chat_history',
                                                    return_messages=True)
        memory_dic[k] = retrieved_memory
    print(f'load_memory_dic \n')
    return memory_dic


def memory_to_list(dm):
    messages = dm.chat_memory.messages
    hl, al = [], []
    for m in messages:
        if m.__class__.__name__ == 'HumanMessage':
            hl.append(m.content)
        elif m.__class__.__name__ == 'AIMessage':
            al.append(m.content)
    if len(al) != len(hl):
        if len(al) == len(hl) + 1:
            hl.append('')
        else:
            print('human 更长')
    return list(zip(hl, al))


def save_periodically(dialogue_dic):
    while True:
        save_history_json(dialogue_dic)
        time.sleep(60)  # 每60秒保存一次


def save_threading(dialogue_dic):
    # 启动定时保存线程
    save_thread = threading.Thread(target=save_periodically, kwargs={'dialogue_dic': dialogue_dic})
    save_thread.daemon = True
    save_thread.start()
