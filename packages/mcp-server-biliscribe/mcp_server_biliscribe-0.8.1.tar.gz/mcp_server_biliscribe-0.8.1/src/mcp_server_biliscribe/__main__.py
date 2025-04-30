"""
包的可执行入口。支持下面两种启动方式：
  1. python -m mcp_server_biliscribe
  2. 安装为控制台命令后直接调用
"""

from .server import serve

def main():
    # 如果需要接收命令行参数，可以在这里接 argparse
    # parser = argparse.ArgumentParser(...)
    # args = parser.parse_args()
    serve()

if __name__ == "__main__":
    main()
