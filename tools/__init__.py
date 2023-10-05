from .text_handler.reqa import get_local_knowledge
from .text_handler.webqa import web_scraping
from langchain.tools.base import StructuredTool
from .easy_functions import easy_funcs

# 获取所有名称
# easy_funcs = dir()
# # 过滤出函数对象
# easy_funcs = [globals()[name] for name in easy_funcs if callable(globals()[name])]
# # 过滤出非私有函数
# easy_funcs = [func for func in easy_funcs if not func.__name__.startswith("_")]
# 其他相对复杂函数的模块
other_funcs = [get_local_knowledge, web_scraping]

tool_list = [StructuredTool.from_function(f) for f in easy_funcs + other_funcs]
