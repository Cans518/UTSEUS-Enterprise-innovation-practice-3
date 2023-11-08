import subprocess
import sys
import os

def merge_time_ranges(time_ranges):
  merged_time_ranges = []
  for i in range(len(time_ranges)):
    if i == 0:
      merged_time_ranges.append(time_ranges[i])
      continue

    previous_time_range = merged_time_ranges[-1]
    current_time_range = time_ranges[i]

    if previous_time_range[1] + 30 >= current_time_range[0]:
      merged_time_ranges[-1] = (previous_time_range[0], current_time_range[1])
    else:
      merged_time_ranges.append(current_time_range)

  return merged_time_ranges

# 检查文件目录下output文件夹是否存在，不存在则创建
if not os.path.exists("output"):
    os.mkdir("output")

def cut_video(input_file, segments):
    i = 1
    for start_time, end_time in segments:
        output_file = f"output/cut{i}.mp4"
        i += 1
        command = f"ffmpeg -ss {start_time} -t {end_time - start_time} -i {input_file} -c copy {output_file} -y"
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    input_file = sys.argv[1]
    info_file_path = "temp/cat_time.in"
    segments = []
    with open(info_file_path, "r") as info_file:
        for line in info_file:
            strat, end = line.strip().split(" - ")
            segments.append((float(strat), float(end)))
    segments = merge_time_ranges(segments)
    cut_video(input_file, segments)
    with open('temp\cat_time_fact.in', 'w') as file:
        for start, end in segments:
            # 输出的时候保留两位小数
            file.write(f"{start:.2f} - {end:.2f}\n")
