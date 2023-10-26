import subprocess
import  sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


def update_progress_bar(progress_bar, current_value, total_value):
    progress = (current_value / total_value) * 100
    progress_bar["value"] = progress
    root.update()


# 创建一个Tkinter窗口
root = tk.Tk()
root.withdraw()

# 选择视频文件
# input_video = filedialog.askopenfilename(title="选择视频文件")
input_video = sys.argv[1]

if input_video:
    # 选择片段信息文件
    #info_file_path = filedialog.askopenfilename(title="选择片段信息文件 (cattime.inf)")

    info_file_path = "cat_time.in"

    if info_file_path:
        # 读取片段信息并存储在一个列表中
        with open(info_file_path, "r") as info_file:
            segments = [line.strip().split() for line in info_file]

        # 创建弹窗
        progress_window = tk.Toplevel()
        progress_window.title("处理进度")

        # 创建进度条
        progress_bar = ttk.Progressbar(progress_window, mode="determinate", length=300)
        progress_bar.grid(row=0, column=0, padx=10, pady=10)

        total_segments = len(segments)

        for i, (start_time, end_time) in enumerate(segments, start=1):
            output_file = f"{i}.mp4"

            # 使用FFmpeg来截取片段
            command = [
                "ffmpeg",
                "-ss", start_time,  # 起始时间
                "-i", input_video,  # 输入视频
                "-to", end_time,  # 结束时间
                "-c:v", "libx264",  # 视频编码器
                "-c:a", "aac",  # 音频编码器
                output_file  # 输出文件名
            ]

            subprocess.run(command)

            # 更新进度条和弹窗信息
            update_progress_bar(progress_bar, i, total_segments)
            progress_window.title(f"处理进度 - {i}/{total_segments} 完成")

        progress_window.destroy()

        # 使用弹窗提示用户
        messagebox.showinfo("提示", "所有片段已截取并保存。")

# 关闭Tkinter窗口
root.destroy()
