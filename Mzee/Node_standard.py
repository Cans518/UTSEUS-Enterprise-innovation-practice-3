import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import ctypes

# 设置DPI感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)

invalid_time = simpledialog.askinteger("输入无效时长", "请输入无效时长，单位为秒")

# 创建一个文件选择弹窗
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

# 弹出文件选择对话框
# file_path = filedialog.askopenfilename()
file_path = "temp/output.mp4"

start_time = 0
end_time = 0

if not file_path:
    print("未选择视频文件")
else:
    # 打开视频文件
    cap = cv2.VideoCapture(file_path)

    # 定义血肉颜色的HSV范围，浅粉色到肉色到红色
    lower_red = np.array([160, 100, 100])
    upper_red = np.array([179, 255, 255])

    # 初始化一个标志变量，用于标记是否发现了血红色
    red_detected = False
    red_time_periods = []
    threshold = 10  # 调整阈值以适应视频

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 将帧转换为HSV颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 创建一个遮罩，将红色部分设置为白色，其余部分设置为黑色
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # 计算遮罩中白色像素的数量
        white_pixel_count = np.sum(mask == 255)

        if white_pixel_count > threshold:
            if not red_detected:
                red_detected = True
                start_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        else:
            if red_detected:
                red_detected = False
                end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                if end_time - start_time > 30 and start_time > invalid_time:
                    red_time_periods.append((start_time, end_time))

    # 释放视频捕捉对象
    cap.release()

    # 打开一个 .in 文件来写入时间段
    with open('temp/cat_time.in', 'w') as file:
        for start, end in red_time_periods:
            # 输出的时候保留两位小数
            file.write(f"{start:.2f} - {end:.2f}\n")
        # 关闭文件
        file.close()

    # 重新打开 .in 文件来删除文件最后一行
    with open('temp/cat_time.in', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        for line in lines[:-1]:
            file.write(line)
        file.close()