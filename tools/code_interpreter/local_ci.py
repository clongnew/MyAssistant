import subprocess
import sys
import os
import re
from codeboxapi.schema import CodeBoxOutput
from codeinterpreterapi import CodeInterpreterSession

# 目前还不太合适，因为 Session 中有太多用到 codebox 的地方了，如果之后需要可能得重写 session 。太费时了

# 吗的，我还不如自己重新写呢

# agent 沿用
# session 应该不用它的，可能用到线程和异步
# run 处理好输出，报错，文件处理，画图如果都是存储起来，是否可以增加画图的
# 在 prompt 中定义存储的位置看看可行不

current_dir = os.path.dirname(os.path.abspath(__file__))


class MyCI(CodeInterpreterSession):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.codebox = MyScript()


class MyScript:
    def __init__(self):
        pass

    def run(self, code: str) -> CodeBoxOutput:
        # 设置一个 chain，总结代码内容，并加入时间戳作为文件夹名称，在本地下加入脚本
        # Create a temporary Python script file to execute the code
        with open("temp_script.py", "w") as temp_file:
            temp_file.write(code)

        try:
            # Execute the script and capture the output
            result = subprocess.run([sys.executable, "temp_script.py"], capture_output=True, text=True, check=True)
            output_content = result.stdout

            return CodeBoxOutput(type='text/plain', content=output_content)
        except subprocess.CalledProcessError as e:
            # Handle execution errors
            error_message = e.stderr
            return CodeBoxOutput(type="error", content=error_message)
        finally:
            # Clean up the temporary script file
            subprocess.run(["rm", "temp_script.py"])

