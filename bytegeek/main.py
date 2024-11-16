import sys
from server import start_server
from client import start_client
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
    
    elif role == "client":
        encoded_ip = 'Ynl0ZWdlZWsuaWN1'   # 服务器IP的Base64编码
        encoded_port = 'Nzg5Nw=='         # 端口的Base64编码
        start_client(encoded_ip, encoded_port)
    
    else:
        print("无效角色，请使用 'server' 或 'client'。")
        sys.exit(1)

if __name__ == "__main__":
    main()
