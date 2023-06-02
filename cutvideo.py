import os
import subprocess
import tkinter.messagebox as messagebox
from tkinter import Tk, filedialog, Entry, Button, Label, StringVar

# 视频文件扩展名列表
video_exts = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']

# 选择视频文件夹
def open_video_folder():
    video_folder.set(filedialog.askdirectory())

# 选择输出文件夹
def open_output_folder():
    output_folder.set(filedialog.askdirectory())

# 判断文件是否是视频
def is_video_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in video_exts

# 切片视频
def split_video():
    for video_file in os.listdir(video_folder.get()):
        if not is_video_file(video_file):
            continue

        # 获取视频时长
        video_path = os.path.join(video_folder.get(), video_file)
        duration_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
        duration = float(subprocess.check_output(duration_cmd, shell=True).decode("utf-8").strip())

        # 获取切片时长
        slice_duration = int(slice_duration_var.get())
        # 获取视频文件名和扩展名
        basename, ext = os.path.splitext(os.path.basename(video_path))

        # 遍历切片
        for index, start_time in enumerate(range(0, int(duration), slice_duration)):
            end_time = min(start_time + slice_duration, int(duration))
            if end_time - start_time < slice_duration:
                continue

            output_name = f"{basename}_{index}{ext}"
            output_path = os.path.join(output_folder.get(), output_name)

            # 调用FFmpeg命令进行切片
            ffmpeg_cmd = f'ffmpeg -ss {start_time} -i "{video_path}" -t {slice_duration} -c copy -threads 4 "{output_path}"'
            subprocess.run(ffmpeg_cmd, shell=True)
        messagebox.showinfo("提示", "视频切片完成！")

# 创建GUI
root = Tk()
root.title("视频切片器")

video_folder = StringVar()
output_folder = StringVar()
slice_duration_var = StringVar()

# 视频文件夹路径
Label(root, text="视频文件夹路径：").grid(row=0, column=0)
Entry(root, textvariable=video_folder).grid(row=0, column=1)
Button(root, text="选择文件夹", command=open_video_folder).grid(row=0, column=2)

# 输出文件夹
Label(root, text="输出文件夹：").grid(row=1, column=0)
Entry(root, textvariable=output_folder).grid(row=1, column=1)
Button(root, text="选择文件夹", command=open_output_folder).grid(row=1, column=2)

# 切片时长
Label(root, text="切片时长（秒）：").grid(row=2, column=0)
Entry(root, textvariable=slice_duration_var).grid(row=2, column=1)

# 开始切片按钮
Button(root, text="开始切片", command=split_video).grid(row=3, column=1)

root.mainloop()
