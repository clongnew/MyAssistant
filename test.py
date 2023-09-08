import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "b5212168ec2f9ec004716b620913db3bc727380839ea8e95f35938e8359ddc6e"
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['all_proxy'] = 'socks5://127.0.0.1:7890'

import openai
# openai.proxy = 'http://proxy.example.org'
openai.proxy = os.getenv('https_proxy')

# from codeinterpreterapi import CodeInterpreterSession
# async def main():
#     # create a session
#     session = CodeInterpreterSession(verbose=True)
#     await session.astart()
#     while True:
#         # generate a response based on user input
#         response = await session.generate_response(
#             "Plot the bitcoin chart of 2023 YTD"
#         )
#         print('response:', response, '\n')
#         print('code_log:', response.code_log[0])
#         # output the response (text + image)
#         print("AI: ", response.content)
#         for file in response.files:
#             print('file:', file, '\n')
#             file.show_image()
#
#         # terminate the session
#         await session.astop()
import asyncio

# asyncio.run(main())

# session = CodeInterpreterSession()
# with session.start():
#     try:
#         response = session.generate_response(
#                 "Plot the bitcoin chart of 2023 YTD"
#             )
#
#         print(response)
#     except:
#         print(1)
# session.stop()
