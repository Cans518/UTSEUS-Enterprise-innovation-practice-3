import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from subprocess import call
from PIL import Image, ImageTk
import ctypes

# 设置DPI感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频处理应用")

        self.video_path = "NULL"

        self.video_path = None
        self.video_capture = None
        self.playing = False

        self.choose_button = tk.Button(root, text="选择视频", command=self.select_video)
        self.play_button = tk.Button(root, text="视频识别", command=self.play)
        self.pause_button = tk.Button(root, text="视频切割", command=self.pause)
        self.reselect_button = tk.Button(root, text="重新选择", command=self.select_video)
        self.next_button = tk.Button(root, text="压缩视频", command=self.process_video)

        # 设置按钮不可见
        self.play_button.grid_remove()
        self.pause_button.grid_remove()
        self.reselect_button.grid_remove()
        self.next_button.grid_remove()

        # 设置按钮样式
        self.set_button_style(self.choose_button, "#4CAF50", "white", ("Helvetica", 14))
        self.set_button_style(self.play_button, "#FFC107", "black", ("Helvetica", 14))
        self.set_button_style(self.pause_button, "#FF5722", "white", ("Helvetica", 14))
        self.set_button_style(self.reselect_button, "#2196F3", "white", ("Helvetica", 14))
        self.set_button_style(self.next_button, "#607D8B", "white", ("Helvetica", 14))

        self.choose_button.grid(row=0, column=0, padx=10, pady=10)
        self.play_button.grid(row=0, column=3, padx=10, pady=10)
        self.pause_button.grid(row=0, column=4, padx=10, pady=10)
        self.reselect_button.grid(row=0, column=1, padx=10, pady=10)
        self.next_button.grid(row=0, column=2, padx=10, pady=10)

        self.video_label = tk.Label(root)
        self.video_label.grid(row=1, column=0, columnspan=5)

    def set_button_style(self, button, bg, fg, font):
        button.configure(bg=bg, fg=fg, font=font)

    def select_video(self):
        video_file_path = filedialog.askopenfilename(filetypes=[("视频文件", "*.mp4")])

        if video_file_path:
            self.video_path = video_file_path
            self.load_and_play_video()
            self.choose_button.grid_remove()

    def load_and_play_video(self):
        if self.video_path:
            self.video_capture = cv2.VideoCapture(self.video_path)
            self.play_video()

    def play_video(self):
        if self.video_path and not self.playing:
            self.playing = True
            self.play_button.grid()
            self.reselect_button.grid()
            self.next_button.grid()
            self.play_button.grid()
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, _ = frame.shape
                if width > 640 or height > 360:
                    frame = cv2.resize(frame, (640, 360))
                    screen_width = root.winfo_screenwidth()
                    screen_height = root.winfo_screenheight()
                    x = (screen_width - 650) // 2  # 将窗口宽度减去窗口宽度后取一半，计算x坐标
                    y = (screen_height - 440) // 2  # 将窗口高度减去窗口高度后取一半，计算y坐标
                    root.geometry(f"650x440+{x}+{y}")  # 设置窗口的大小和位置
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.video_label.config(image=photo)
                self.video_label.image = photo
                self.video_label.after(10, self.play_video)
            else:
                self.playing = False
                self.play_button.config(text="播放", command=self.play)
                self.video_capture.release()

    def pause(self):
        if self.video_path:
            if self.video_path != "NULL":
                self.video_capture.release()
                call(["python", "video_cut.py", self.video_path])
                messagebox.showinfo("处理完成", "视频处理完成!")
            else:
                messagebox.showerror("错误", "未选择视频文件!")

    def play(self):
        if self.video_path:
            if self.video_path != "NULL":
                self.video_capture.release()
                call(["python", "Node_standard.py"])
                messagebox.showinfo("处理完成", "视频处理完成!")
            else:
                messagebox.showerror("错误", "未选择视频文件!")

    def process_video(self):
        if self.video_path:
            if self.video_path != "NULL":
                self.video_capture.release()
                call(["python", "preprocessing.py", self.video_path])
                messagebox.showinfo("处理完成", "视频处理完成!")
            else:
                messagebox.showerror("错误", "未选择视频文件!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 700) // 2  # 将窗口宽度减去窗口宽度后取一半，计算x坐标
    y = (screen_height - 90) // 2  # 将窗口高度减去窗口高度后取一半，计算y坐标
    root.geometry(f"700x90+{x}+{y}")  # 设置窗口的大小和位置
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
