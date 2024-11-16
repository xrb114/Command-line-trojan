#进程拦截
import win32gui
import win32con
import json
import os
import time

# 配置文件路径
RULES_FILE = "intercept_rules.json"

# 加载拦截规则
def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 保存拦截规则
def save_rules(rules):
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=4)

# 获取所有窗口
def get_all_windows():
    """
    获取所有窗口的句柄、标题和类名
    """
    windows = []
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):  # 判断窗口是否可见
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if title:  # 排除无标题窗口
                windows.append((hwnd, title, class_name))
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

# 列出所有窗口
def list_windows():
    """
    列出当前所有窗口标题和类名
    """
    windows = get_all_windows()
    print("\n=== 当前活动窗口列表 ===")
    for idx, (hwnd, title, class_name) in enumerate(windows):
        print(f"{idx + 1}. 标题: {title} | 类名: {class_name}")
    return windows

# 关闭窗口
def close_window(hwnd):
    """
    关闭指定窗口
    """
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

# 开始拦截
def start_intercept(rules):
    """
    实时检测并拦截选定的窗口
    """
    print("\n开始拦截...")
    try:
        while True:
            windows = get_all_windows()
            for hwnd, title, class_name in windows:
                if title in rules:
                    print(f"[拦截] 关闭窗口: {title}")
                    close_window(hwnd)
            time.sleep(1)  # 每秒扫描一次
    except KeyboardInterrupt:
        print("\n拦截已停止!")

# 主程序
def main():
    rules = load_rules()
    print(f"\n已加载本地拦截规则: {rules}")

    while True:
        print("\n=== 操作选项 ===")
        print("1. 查看当前活动窗口")
        print("2. 添加拦截规则（选择窗口标题）")
        print("3. 删除拦截规则")
        print("4. 查看拦截规则")
        print("5. 开始拦截")
        print("6. 退出程序")
        choice = input("请输入选项: ")

        if choice == "1":
            list_windows()
        elif choice == "2":
            windows = list_windows()
            try:
                indices = input("输入需要拦截的窗口序号（用逗号分隔，例如 1,3,5）: ")
                indices = [int(idx.strip()) - 1 for idx in indices.split(",")]
                new_rules = [windows[idx][1] for idx in indices]
                rules.extend(new_rules)
                rules = list(set(rules))  # 去重
                save_rules(rules)
                print(f"规则已更新: {rules}")
            except (ValueError, IndexError):
                print("输入有误，请重试!")
        elif choice == "3":
            print("\n当前拦截规则:")
            for i, rule in enumerate(rules):
                print(f"{i + 1}. {rule}")
            try:
                index = int(input("输入要删除的规则序号: ")) - 1
                removed_rule = rules.pop(index)
                save_rules(rules)
                print(f"已删除规则: {removed_rule}")
            except (ValueError, IndexError):
                print("输入无效，请重试!")
        elif choice == "4":
            print("\n当前拦截规则:")
            for i, rule in enumerate(rules):
                print(f"{i + 1}. {rule}")
        elif choice == "5":
            if rules:
                start_intercept(rules)
            else:
                print("未定义任何拦截规则，请先添加规则!")
        elif choice == "6":
            print("退出程序!")
            break
        else:
            print("无效选项，请重试!")

if __name__ == "__main__":
    main()
