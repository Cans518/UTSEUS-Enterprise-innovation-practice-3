from tkinter import ttk
import sys
import subprocess
import re
from ttkthemes import ThemedTk


def center_window(window):
    window.update_idletasks()
    w = window.winfo_width()
    h = window.winfo_height()
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('+%d+%d' % (x, y))


# 创建一个带主题的Tkinter窗口
root = ThemedTk(theme="equilux")

# 隐藏主窗口
root.withdraw()

# 打开文件选择对话框，让用户选择视频文件
# file_path = filedialog.askopenfilename(title="选择要压缩的视频文件")

file_path = sys.argv[1]
print(file_path)


if file_path:
    # 构建FFmpeg命令
    output_file = "output.mp4"  # 硬编码的输出文件名
    command = [
        "ffmpeg",
        "-i", file_path,
        "-vf", "scale=640:360,fps=12",
        "-b:v", "500k",
        "-r", "12",
        "-c:a", "aac",
        "-strict", "-2",
        "-y",  # 添加 -y 参数以自动覆盖现有文件
        output_file
    ]

    # 创建一个Tkinter窗口来显示进度条
    progress_window = ThemedTk(theme="equilux")
    progress_window.title("压缩进度")

    # 让窗口居中
    center_window(progress_window)

    # 创建一个带有美观主题的进度条
    style = ttk.Style()
    style.theme_use("equilux")
    style.configure("TProgressbar", thickness=30)

    progress_bar = ttk.Progressbar(progress_window, mode="determinate", style="TProgressbar", length=300)
    progress_bar.grid(row=0, column=0, padx=10, pady=10)


    def update_progress(output):
        # 从FFmpeg输出中提取进度信息
        matches = re.findall(r"frame=\s*(\d+)", output)
        if matches:
            frame_number = int(matches[-1])
            progress = (frame_number / total_frames) * 100
            progress_bar["value"] = progress
            root.update()


    # 获取视频的总帧数
    ffprobe_command = [
        "ffprobe",
        "-v", "error",
        "-count_frames",
        "-select_streams", "v:0",
        "-show_entries", "stream=nb_frames",
        "-of", "default=nokey=1:noprint_wrappers=1",
        file_path
    ]
    ffprobe_process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE)
    total_frames = int(ffprobe_process.stdout.read().decode("utf-8"))

    # 使用subprocess运行FFmpeg命令，并更新进度
    ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                      encoding="utf-8")

    for line in ffmpeg_process.stderr:
        update_progress(line)

    # 设置进度条为100%
    while progress_bar["value"] < 100:
        progress_bar["value"] += 10
        root.update()

    # 关闭Tkinter窗口
    progress_window.destroy()

    print("视频压缩完成，保存为", output_file)
else:
    print("未选择视频文件")

# 关闭tkinter窗口
root.destroy()
