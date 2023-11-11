import os
import sys
import subprocess

if not os.path.exists("temp"):
    os.mkdir("temp")

def compress_video(input_file, output_file):
  # 设置视频分辨率为 240×160。
  resolution = "-vf scale=240:160"
  # 设置视频数据速率为 58kbps。
  video_bitrate = "-b:v 58k"
  # 设置视频总比特率为 250kbps。
  total_bitrate = "-b:a 250k"
  # 设置视频帧数为 12 帧。
  frame_rate = "-r 12"
  # 去掉声音。
  audio_disable = "-an"
  
  # 视频压缩命令
  command = f"ffmpeg -i {input_file} {resolution} {video_bitrate} {total_bitrate} {frame_rate} {audio_disable} {output_file}  -hwaccel nvenc -c:v h264_nvenc -preset ultrafast -y  "

  print("开始压缩视频...")
  # 执行视频压缩命令
  subprocess.call(command, shell=True)
  print("视频压缩完成。")

if __name__ == "__main__":
  # 获取视频文件路径,路径来自于命令行参数
  file_path = sys.argv[1]
  output_file = "temp/output.mp4"
  compress_video(file_path, output_file)
