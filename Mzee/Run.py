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
        self.root.title("手术视频识别")

        self.video_path = "NULL"

        self.video_path = None
        self.video_capture = None
        self.playing = False

        self.video_label = tk.Label(root)
            # 添加使用提示标签
        self.tip_label = tk.Label(root, text="请单击按钮选择需要处理的视频\n选择完成后自带跳转到下一页面", font=("Helvetica", 12))
        self.tip_label_2 = tk.Label(root, text="在点击按钮以后耐心等待，请勿操作", font=("Helvetica", 12),fg="red")
        self.choose_button = tk.Button(root, text="选择视频", command=self.select_video)
        self.recognize_button = tk.Button(root, text="视频识别", command=self.recognize_video)
        self.cutvideo_button = tk.Button(root, text="视频切割", command=self.cut_video)
        self.reselect_button = tk.Button(root, text="重新选择", command=self.select_video)
        self.comperssed_button = tk.Button(root, text="压缩视频", command=self.comperssed_video)

        # 设置按钮样式
        self.set_button_style(self.choose_button, "#4CAF50", "white", ("Helvetica", 14))
        self.set_button_style(self.recognize_button, "#FFC107", "black", ("Helvetica", 14))
        self.set_button_style(self.cutvideo_button, "#FF5722", "white", ("Helvetica", 14))
        self.set_button_style(self.reselect_button, "#2196F3", "white", ("Helvetica", 14))
        self.set_button_style(self.comperssed_button, "#607D8B", "white", ("Helvetica", 14))

        self.choose_button.grid(row=0, column=2, padx=10, pady=10)
        self.tip_label.grid(row=1, column=0, columnspan=5, padx=20, pady=10)

        # 设置按钮不可见
        self.recognize_button.grid_remove()
        self.cutvideo_button.grid_remove()
        self.reselect_button.grid_remove()
        self.comperssed_button.grid_remove()

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
            self.recognize_button.grid(row=4, column=3, padx=10, pady=10)
            self.cutvideo_button.grid(row=4, column=4, padx=10, pady=10)
            self.reselect_button.grid(row=4, column=1, padx=10, pady=10)
            self.comperssed_button.grid(row=4, column=2, padx=10, pady=10)
            self.tip_label.config(text="请依次点击按钮进行视频识别、视频切割、视频压缩\n如果选择错误的视频，请重新选择\n处理完成后直接关闭掉程序")
            self.tip_label_2.grid(row=2, column=1, columnspan=5)
            self.choose_button.grid_remove()
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, _ = frame.shape
                if width > 640 or height > 360:
                    frame = cv2.resize(frame, (640, 360))
                    screen_width = root.winfo_screenwidth()
                    screen_height = root.winfo_screenheight()
                    winodws_width_2 = 645
                    winodws_height_2 = 590
                    x = (screen_width - winodws_width_2) // 2  # 将窗口宽度减去窗口宽度后取一半，计算x坐标
                    y = (screen_height - winodws_height_2) // 2  # 将窗口高度减去窗口高度后取一半，计算y坐标
                    root.geometry(f"{winodws_width_2}x{winodws_height_2}+{x}+{y}")  # 设置窗口的大小和位置
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.video_label.config(image=photo)
                self.video_label.image = photo
                self.video_label.grid(row=5, column=1, columnspan=4)
                # self.video_label.after(10, self.play_video)

    def cut_video(self):
        if self.video_path:
            if self.video_path != "NULL":
                self.video_capture.release()
                call(["python", "video_cut.py", self.video_path])
                messagebox.showinfo("剪辑完成", "视频剪辑完成!")
            else:
                messagebox.showerror("错误", "未选择视频文件!")

    def recognize_video(self):
        if self.video_path:
            if self.video_path != "NULL":
                self.video_capture.release()
                call(["python", "Node_standard.py"])
                messagebox.showinfo("识别完成", "视频识别完成!")
            else:
                messagebox.showerror("错误", "未选择视频文件!")

    def comperssed_video(self):
        if self.video_path:
            if self.video_path != "NULL":
                self.video_capture.release()
                call(["python", "preprocessing.py", self.video_path])
                messagebox.showinfo("压缩完成", "压缩处理完成!")
            else:
                messagebox.showerror("错误", "未选择视频文件!")

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    winodws_width = 340
    winodws_height = 150
    x = (screen_width - winodws_width) // 2  # 将窗口宽度减去窗口宽度后取一半，计算x坐标
    y = (screen_height - winodws_height) // 2  # 将窗口高度减去窗口高度后取一半，计算y坐标
    root.geometry(f"{winodws_width}x{winodws_height}-{x}-{y}")  # 设置窗口的大小和位置
    app = VideoPlayerApp(root)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
