import os
import sys

# 现在不走代理，用 api2d 来访问，避免代理很多麻烦。对于需要访问外网的工具，在其中设置外网的相关设置，使用完 pop
# os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "b5212168ec2f9ec004716b620913db3bc727380839ea8e95f35938e8359ddc6e"
os.environ["OPENAI_API_KEY"] = 'fk200821-RPW7NmOKUwdGFU7w6aaN54hyn2OkUKYt'
os.environ['OPENAI_API_BASE'] = 'https://oa.api2d.net/v1'

# 0。设置新文件，将本地解释器的雏形加上，设为
# 1。搞定本地启用特定 kernel 的 box
# 2. 了解


# 我的计划
# 设置一个详细探索器，给一段提示，给出最终的分析报告和相应代码
# 代码解释器只是它的工具之一，可以每天用于执行或者在主界面加一个标签页，想起要探索什么到时直接输入即可
# 建议与 tools 并列，新开一个目录，存储报告直接在它下方而非代码解释器下方
# 关于代码解释器下方的存储，response: content, files, code_log
# 每执行一次 session，在 code_interpreter/results 下方新建一个以这次任务简略命名的文件夹，存储上述3个为json，并额外增肌一个py文件。在 run_handler 最后统一存储
# 这3个文件的命名，根据 output.type 和时间戳来决定，
# session 以json 形式返回，要求包含文件存储地址

# 现在主要是探索 agent 怎么构造
# prompts: 研究新领域，可以去看一下了解行业几步法，然后给出能够更好给出资料，分析结果


# def save(path):
#     if not path.startswith("/"):
#         path = f"./{path}"
#     with open(path, "wb") as f:
#         f.write(content)


from codeinterpreterapi import CodeInterpreterSession
from codeboxapi.box.localbox import LocalBox

# 测试一下脚本执行代码的效果
code = """
# Plot the closing price
import matplotlib.pyplot as plt 
plt.figure(figsize=(14,7))
plt.title('Bitcoin Price 2023')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.show()

"""


# class MyCI(CodeInterpreterSession):
#     def __int__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.codebox = LocalBox()
#
#
# async def main():
#     # create a session
#     session = CodeInterpreterSession(verbose=True)
#     await session.astart()
#     for i in range(3):
#         # generate a response based on user input
#         response = await session.generate_response(
#             "给我一个 matplotlib 的简单案例"
#         )
#
#         # output the response (text + image)
#         print('response:', response, '\n')
#         # 直接将 code_log 存为日志
#         # 每开启一个任务，
#         print('code_log:', response.code_log)
#         print("AI: ", response.content)
#         for file in response.files:
#             print('file:', file, '\n')
#             file.show_image()
#             # 如果这个存储方式的目录合适
#             file.save(path='codeinterpreter_files')
#
#         # terminate the session
#         await session.astop()


import asyncio

# asyncio.run(main())

from codeboxapi import CodeBox


# startup and automatically shutdown a new codebox
with CodeBox() as codebox:
    # check if it's running
    print(codebox.status())

    # run some code
    codebox.run(code)
    # Hello, World!




