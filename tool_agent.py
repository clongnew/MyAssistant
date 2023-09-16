from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from tools import tool_list
from langchain.tools.base import StructuredTool
from prompts import message_funcs
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)


# 尝试以下：1。 报错内容更具体，直接捕获 2。工具里不再直接包含 run_code 3。给的 prompt 要求重新执行 4。或者将原代码直接返回
# 这个也是工具，但由于初始化 agent 需要这些工具，因此在这里使用
def create_agent(memory=None, sys_message='You are a helpful AI assistant.', mytools=None):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", streaming=True,
                     callbacks=[FinalStreamingStdOutCallbackHandler()])
    system_message = SystemMessage(content=sys_message)
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
        "system_message": system_message,
    }
    if not memory:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    if not mytools:
        mytools = tool_list

    agent = initialize_agent(
        mytools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        # system_message=system_message,
        memory=memory,
    )
    return agent


# 根据内置 prompt 创建 agent
def create_tool_agent(message_func):
    agent = create_agent(sys_message=message_func())

    def f():
        return agent.run

    f.__name__ = message_func.__name__
    f.__doc__ = message_func.__doc__

    return StructuredTool.from_function(f)


tool_agent_list = [create_tool_agent(f) for f in message_funcs]
