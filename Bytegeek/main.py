import sys
from server import start_server

import base64

def main():
    if len(sys.argv) < 2:
        print("用法: python main.py server|client")
        sys.exit(1)

    role = sys.argv[1].lower()

    if role == "server":
        host = input("请输入连接地址 (默认 'localhost')：") or ''
        port = int(input("请输入服务器端口号 (默认 7897)：") or 7897)
        start_server(host, port)
    

    else:
        print("无效角色，请使用 'server' 或 'client'。")
        sys.exit(1)

if __name__ == "__main__":
    main()