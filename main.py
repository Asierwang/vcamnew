"""
虚拟摄像头主程序
Windows虚拟摄像头控制器
"""
import sys
import os

# 添加当前目录到Python路径，确保能正确导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from gui import main


if __name__ == '__main__':
    main()