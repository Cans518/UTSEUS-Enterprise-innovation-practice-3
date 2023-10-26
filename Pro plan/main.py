import cv2
import imageio.plugins.opencv
import numpy as np
from moviepy.editor import VideoFileClip
import os
import tkinter as tk

def UI():
    rook = tk.Tk()
    rook.geometry("600x200")
    rook.title("请确定筛选阈值")
    label_POS = tk.Label(rook, text="文件位置", font=("宋体", 25), fg="red")
    label_POS.grid(row = 1, column = 1)
    label_HSV = tk.Label(rook, text= "hsv阈值", font=("宋体",25),fg="red")
    label_HSV.grid(row = 2, column = 1)
    label_RGB = tk.Label(rook, text="rgb阈值", font=("宋体", 25), fg="red")
    label_RGB.grid(row = 3, column = 1)

    entry_POS = tk.Entry(rook, font=("宋体", 25), fg="red")
    entry_POS.grid(row=1, column=2)

    entry_HSV = tk.Entry(rook, font=("宋体", 25), fg="red")
    entry_HSV.grid(row=2, column=2)

    entry_RGB = tk.Entry(rook, font=("宋体",25),fg="red")
    entry_RGB.grid(row = 3, column = 2)

    def get_input():
        global video_src_path
        video_src_path = entry_POS.get()
        global HSV_threshold
        HSV_threshold = float(entry_HSV.get())
        global RGB_threshold
        RGB_threshold = float(entry_RGB.get())
        rook.destroy()

    button = tk.Button(rook, text="确定", width=8 ,height=3, command=get_input)
    button.grid(row=4, column=2)

    rook.mainloop()

def Video_cut(start_time,end_time,cnt):
    new_video = VideoFileClip(video_src_path).subclip(start_time,end_time)
    new_video.write_videofile("F:/Programme/Surgical recognition/new_video/{}.mp4".format(cnt))

def Histogram(image_1, image_2):
    image_hsv_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2HSV)
    image_hsv_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2HSV)
    channels = [0]
    hist_hsv_1 = cv2.calcHist([image_hsv_1], channels, None, [256], [0.0, 255.0])
    hist_hsv_2 = cv2.calcHist([image_hsv_2], channels, None, [256], [0.0, 255.0])
    hist_bgr_1 = cv2.calcHist([image_1], channels, None, [256], [0.0, 255.0])
    hist_bgr_2 = cv2.calcHist([image_2], channels, None, [256], [0.0, 255.0])
    degree_hsv = cv2.compareHist(hist_hsv_1, hist_hsv_2, method=cv2.HISTCMP_CORREL)
    degree_hsv = abs(degree_hsv)
    degree_bgr = cv2.compareHist(hist_bgr_1, hist_bgr_2, method=cv2.HISTCMP_CORREL)
    degree_bgr = abs(degree_bgr)
    return degree_hsv ,degree_bgr

def GetVideo(input_video):

    cap = cv2.VideoCapture(input_video)
    frame_cnt = 1
    last_times = 0
    cnt = 0
    success , frame = cap.read()
    last_frame = frame
    while(success):
        success , frame = cap.read()
        frame_cnt += 1
        if frame_cnt % 50 != 0:
            continue

        diff_hsv, diff_bgr = Histogram(np.uint8(last_frame),np.uint8(frame))
        cv2.imshow('fr',frame)
        keyboard = cv2.waitKey(1)
        if keyboard == 27:
            return
        #0.15and0.5
        if diff_hsv < HSV_threshold and diff_bgr < RGB_threshold:
            #print(diff_bgr)
            times = int(frame_cnt / 50)
            if times - last_times > 3:
                cnt += 1
                cv2.imwrite('F:\Programme\Surgical recognition\pic\{}.jpg'.format(int(frame_cnt/50-1)) , last_frame)
                cv2.imwrite('F:\Programme\Surgical recognition\pic\{}.jpg'.format(int(frame_cnt/50)) , frame)
                last_times = times
                #Video_cut(last_times,times,cnt)

        last_frame = frame


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UI()
    GetVideo(video_src_path)


