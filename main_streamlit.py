"""
1. 理解它是当触发了回调函数，就会从上到下重新执行一遍。所以当时 agent 总报错，
    因为重新执行的时候，agent 这些 session_state 就被初始话了。所以必须要声明之前没有这样的 key
    而 hd_option 的 options 选项，也会随着重新运行而加入新的内容
    之前 hd 能重写而 clear 不行，也是因为重新开了一个 container 来写历史记录。当然，如果接下来再写一个 container ，它就是额外的一个了，不会起到删除作用
"""
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ["OPENAI_API_KEY"] = 'fk200821-RPW7NmOKUwdGFU7w6aaN54hyn2OkUKYt'
os.environ['OPENAI_API_BASE'] = 'https://oa.api2d.net/v1'
os.environ["SERPAPI_API_KEY"] = "b5212168ec2f9ec004716b620913db3bc727380839ea8e95f35938e8359ddc6e"

import streamlit as st
from main_functions import check_name, generate_name, memory_to_list, create_main_agent, load_history_memory
from langchain.callbacks import StreamlitCallbackHandler

# 页面布局
st.set_page_config(page_title='Dragon Assistant',
                   page_icon="🦖",
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None
                   )
# 好像还必须加这个，不然对应的包导入不了
main_agent = create_main_agent()
dialogue_dic = load_history_memory()
ct_option = st.empty()

st.session_state['qa'] = ct_option
st.session_state['human'] = 'Human'
st.session_state['ai'] = 'AI'
if 'main_agent' not in list(st.session_state.keys()):
    print('reload_agent', list(st.session_state.keys()), '\n')
    st.session_state['main_agent'] = main_agent
if 'dialogue_dic' not in st.session_state:
    print('reload_dic', list(st.session_state.keys()), '\n')
    st.session_state['dialogue_dic'] = dialogue_dic


# memory 的相互转化，可能需要session_state
def memory2chat(name):
    memory = st.session_state.dialogue_dic[name]
    st.session_state.main_agent = create_main_agent(memory=memory)
    messages = memory.chat_memory.messages
    # 要不要qa
    with st.session_state.qa.container():
        for m in messages:
            role = st.session_state.human \
                if m.__class__.__name__ == 'HumanMessage' else st.session_state.ai
            st.chat_message(role).write(m.content)


def clear_qa():
    st.session_state.main_agent = create_main_agent(memory=None)
    st.session_state.qa.empty()


# 生成回答
def q_and_a(query, current_name):
    st_callbacks = StreamlitCallbackHandler(st.empty().container().chat_message(st.session_state.ai))
    answer = st.session_state.main_agent.run(query, callbacks=[st_callbacks])
    if not current_name:
        current_name = check_name(generate_name(query), st.session_state.dialogue_dic)
    st.session_state.dialogue_dic[current_name] = st.session_state.main_agent.memory
    # print('d_d2', st.session_state.dialogue_dic, '\n', 'm_a2', st.session_state.main_agent, '\n')
    with st.empty().container():
        st.chat_message(st.session_state.ai).write(answer)


# 历史对话
with st.sidebar:
    hd_option = st.selectbox(label='history_chat',
                             options=[""] + list(st.session_state.dialogue_dic.keys()), key='hd')
    st.markdown("**note: choose blank to start a new chat**")
    view_messages = st.expander("View the message contents in session state")

    if hd_option:
        memory2chat(hd_option)
    else:
        clear_qa()

    with view_messages:
        view_messages.json({k: v for k, v in st.session_state.items()})

# 输入
if query := st.chat_input():
    st.empty().container().chat_message(st.session_state.human).write(query)
    q_and_a(query, hd_option)
