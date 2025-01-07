# -*- coding: utf-8 -*-
# @Time : 2024/10/9 上午9:12
# @Author : D.N. Huang
# @Email : CarlCypress01@gmail.com
# @File : setup.py
# @Project : fitness_evaluation
import subprocess
import sys


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing: {command}\n{e.stderr}")
        sys.exit(1)


# 1. 安装 ultralytics==8.2.95
def install_ultralytics():
    print("Installing ultralytics==8.2.95...")
    run_command("pip install ultralytics==8.2.95")


# 2. 修改ultralytics相关配置文件
def modify_ultralytics_config():
    print("Modifying ultralytics configuration files...")
    # 给shell脚本执行权限
    run_command("chmod +x ./replace_file/replace_files.sh")
    # 执行替换文件脚本
    run_command("./replace_file/replace_files.sh")


# 3. 更新 mindtorch
def update_mindtorch():
    print("Updating mindtorch...")
    # 卸载mindtorch（如果存在）
    run_command("pip uninstall -y mindtorch")
    # 安装新的mindtorch版本
    run_command("pip install git+https://openi.pcl.ac.cn/OpenI/MSAdapter.git@f7b6b6eff6")


if __name__ == "__main__":
    # 执行各步骤
    install_ultralytics()
    modify_ultralytics_config()
    update_mindtorch()
