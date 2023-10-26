import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# 创建一个文件选择弹窗
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

# 弹出文件选择对话框
# file_path = filedialog.askopenfilename()
file_path = "output.mp4"

if not file_path:
    print("未选择视频文件")
else:
    # 打开视频文件
    cap = cv2.VideoCapture(file_path)

    # 定义红色的颜色范围
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([100, 100, 255])

    # 初始化一个标志变量，用于标记是否发现了血红色
    red_detected = False
    red_time_periods = []
    threshold = 100  # 调整阈值以适应您的视频

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

        # 如果白色像素数量足够多，认为发现了血红色
        if white_pixel_count > threshold:
            if not red_detected:
                red_detected = True
                start_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        else:
            if red_detected:
                red_detected = False
                end_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                red_time_periods.append((start_time, end_time))

    # 释放视频捕捉对象
    cap.release()

    # 打开一个 .inf 文件来写入时间段
    with open('cat_time.in', 'w') as file:
        for start, end in red_time_periods:
            file.write(f"{start}秒 - {end}秒\n")
