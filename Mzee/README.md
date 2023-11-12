# UTSEUS-Enterprise-innovation-practice-3

## 仓库简述

> ​	本仓库内容为2023年上海大学中欧工程技术学院23年秋季学期`企业创新项目实战`课程的第三次课题项目的实现。

> ​	可在本人主页找到上次课题项目的数据处理工具，[跳转链接](https://github.com/Cans518/UTSEUS-Enterprise-innovation-practice-2)

> ​	本工具完全使用`python`进行数据的读取与处理，使用`openCV`库做视频的识别，使用`numpy`进行数据的处理，使用`subprocess`、`ctypes`、`tkinter`和`sys`进行窗口UI的简单设计，使用`FFmpeg`开源软件作为视频处理与剪辑的工具。

​	**在使用本工具前请确保您的电脑上已经安装`python`、上面提到的软件包以及较新版本的`FFmpeg`工具**

​	[FFmpeg官网](https://www.ffmpeg.org/)

​	[FFmpeg Github主页](https://github.com/FFmpeg/FFmpeg)

​	首先感谢开源软件的各位作者为本项目提供的代码和文档支持。



## 任务简述

> ​	对于日益增长的，人民对于新生活，好生活的向往与追求。人们对于医疗尤其是高端医疗手术的需求越来越高，但是偏远地区的医生或许有高超的手艺，但受限于机器、眼界和没有具体了解过高难度手术的难点和细节。
>
> ​	手术直播和手术录播成为了解决这一痛点的有力手段。
>
> ​	但是大量的高清录像中有很多的不必要的片段与无用的时间，为观看与储存带来了大量的成本与负担。目前一种能够自动剪辑出一段医学手术录像中的有效片段就成了急需。
>
> ​	本仓库工具的目标就是能够粗略地将实施手术片段进行分片与切割。



## 使用工具

### Python

#### subprocess、ctypes、tkinter、sys

- subprocess
  - 这个库的使用是将shell命令发送到命令行调用`FFmpeg`
  - 当然这个库也是用来多文件脚本调用和给参
- ctypes
  - 这个库用来适配当前电脑的DPI，使UI清晰显示
- tkinter
  - 实现UI操作的库
- sys
  - 脚本用来读取命令行给进的参数
  - 用来与`FFmpeg`进行交互

#### OpenCV

- 这是目前最受欢迎并且应该最广的计算机处理库同时支持python、C\C++等多种语言
- 这里是使用OpenCV-python进行视频的操作和识别

#### numpy

- 在计算机中图像就是数组所以我们处理图像必然涉及到numpy进行数据处理。

### FFmpeg

> ​	FFmpeg 是一个开放源代码的自由软件，可以执行音频和视频多种格式的录影、转换、串流功能，包含了libavcodec——这是一个用于多个项目中音频和视频的解码器函式库，以及libavformat——一个音频与视频格式转换函式库。
​	“FFmpeg”这个单词中的“FF”指的是“Fast Forward（快速前进）”。“FFmpeg”的项目负责人在一封回信中说：“Just for the record, the original meaning of "FF" in FFmpeg is "Fast Forward"...”
​	这个项目最初是由法国程序员法布里斯·贝拉（Fabrice Bellard）发起的，而现在是由迈克尔·尼德梅尔（Michael Niedermayer）在进行维护。许多FFmpeg的开发者同时也是MPlayer项目的成员，FFmpeg在MPlayer项目中是被设计为服务器版本进行开发。

​	以鄙人的拙见而言`FFmpeg`是最有价值的开源项目之一，它为C/C++，Python以及其它常用语言提供了一种方便、快捷且高性能的本地、网络视频的流操作工具。

​	我们在这里使用`FFmpeg`来进行视频的压制与片段的剪辑。

- 视频压制命令：

```shell
ffmpeg -i {input_file} {resolution} {video_bitrate} {total_bitrate} {frame_rate} {audio_disable} {output_file}  -hwaccel nvenc -c:v h264_nvenc -preset ultrafast -y  
```



```txt
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
```

- 视频片段剪辑命令：

```shell
ffmpeg -ss {start_time} -t {end_time - start_time} -i {input_file} -c copy {output_file} -y
```



- 这里是对应的本地选择的本地视频。
- 如果需要剪辑网络流视频也是可以进行剪辑的，甚至对于直播的视频流都可以进行实时的转录与剪辑。



## 完成思路

1. 首先对需要处理的视频进行预处理，包括视频的分辨率、帧率、码率、音频编码等。
2. 压缩需要处理的视频文件作为视频识别的输入。
   1. 压缩格式为：`mp4`
   2. 压缩码率为：`500kbps`
   3. 压缩帧率为：`12fps`
   4. 压缩分辨率为：`240*160`
   5. 去掉音频
3. 对压缩后的文件进行识别。
4. 识别出需要片段的时间段，将时间戳存入缓存文件。
5. 利用缓存文件进行剪辑。



## 识别算法逻辑

- 根据需要识别的视频的特征，我们需要将正在进行手术的视频提取出来。
  - 通俗来讲我们一般认为出现大面积的血肉的地方就是需要进行手术的地方。
  - 我们可以利用`OpenCV`库来进行视频的识别，通过`OpenCV`库的`HSV`颜色空间来进行颜色的识别。
  - 我们可以将视频分为若干个区域，然后对每个区域进行颜色的识别，如果颜色的识别结果符合我们设定的阈值，那么我们就认为这个区域是需要进行手术的区域。
- 在识别完成后将对应的秒数存入缓存文件中。
- 利用缓存文件进行剪辑。


## 项目结构

```python
.
├── temp/cat_time.in
├── temp/cat_time_fact.in
├── temp/output.mp4
├── output/picture
├── output/video
├── Run.py
├── Node_standard.py
├── preprocessing.py
├── video_cut.py
├── Run.bat
└── README.md
```
- `temp`文件夹是用来存放临时文件，其中`cat_time.in`是用来存放需要识别的时间段的缓存文件，`cat_time_fact.in`是用来存放需要剪辑的时间段的缓存文件，`output.mp4`是用来存放剪辑后的视频文件。
- `output`文件夹是用来存放剪辑后的图片和视频文件。
- `Run.py`是UI实现的程序，`Node_standard.py`是用来进行视频的识别，`preprocessing.py`是用来进行视频的压缩，`video_cut.py`是用来进行视频的剪辑。
- `Run.bat`是Windows平台下运行的批处理文件。
- `README.md`是本项目的说明文档。

