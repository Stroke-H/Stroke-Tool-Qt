import os
import re


def check_files_in_folder(folder_path):
    # 正则表达式，匹配"x.mp4"格式，其中x是阿拉伯数字
    mp4_pattern = re.compile(r'^(\d+)\.mp4$')
    mp4_files = []
    non_mp4_files = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        match = mp4_pattern.match(filename)
        if match:
            # 提取x部分（数字），并转换为整数
            mp4_files.append(int(match.group(1)))
        else:
            # 标记不符合"x.mp4"格式的文件
            non_mp4_files.append(filename)

    # 对提取到的数字部分进行排序
    mp4_files.sort()

    # 检查是否有缺失的数字
    missing_files = []
    for i in range(mp4_files[0], mp4_files[-1] + 1):
        if i not in mp4_files:
            missing_files.append(f"{i}.mp4")

    return non_mp4_files, missing_files


# 使用示例
folder_path = r"C:\Users\hmh70\Desktop\test"  # 替换为你的文件夹路径
non_mp4_files, missing_files = check_files_in_folder(folder_path)

print("非'x.mp4'格式的文件:", non_mp4_files)
print("缺失的文件:", missing_files)
