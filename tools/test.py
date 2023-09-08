import os

# 获取当前脚本所在目录的父目录路径
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
print(current_directory, parent_directory)

# 新文件夹的名称
new_folder_name = "assist_refer_files"

# 创建新文件夹的完整路径
new_folder_path = os.path.join(parent_directory, new_folder_name)

os.makedirs(new_folder_path, exist_ok=True)
