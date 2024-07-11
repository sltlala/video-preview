import cv2
import os
from moviepy.editor import VideoFileClip
from PIL import Image
import argparse

def capture_frame(video_path, output_path, time):
    """
    使用opencv从视频文件中获取指定时间点的截图并保存为图像文件。
    
    :param video_path: 视频文件路径
    :param output_path: 输出图像文件路径
    :param time: 截图时间点（秒数）
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(time * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    if ret:
        cv2.imwrite(output_path, frame)
        print(f"截图已保存至 {output_path}")
    else:
        print(f"无法读取视频文件或时间点超出视频长度: {time} 秒")
    
    cap.release()
    # 将OpenCV的BGR图像转换为RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame_rgb)
    
def get_video_info(video_path):
    """
    获取视频文件信息，包括文件大小、视频分辨率、时长和编码。
    
    :param video_path: 视频文件路径
    :return: 包含视频信息的字典
    """
    video_info = {}
    
    # 获取文件大小
    video_info['file_size'] = os.path.getsize(video_path)
    
    # 使用 moviepy 获取视频信息
    clip = VideoFileClip(video_path)
    video_info['duration'] = clip.duration
    video_info['resolution'] = (clip.w, clip.h)
    video_info['fps'] = clip.fps

    return video_info

def check_quality_range(value):
    """
    检查输入的质量值是否在1到10之间。
    
    :param value: 输入的质量值
    :return: 如果输入的质量值在1到10之间，则返回该值；否则抛出异常
    """
    ivalue = int(value)
    if ivalue < 1 or ivalue > 10:
        raise argparse.ArgumentTypeError(f"{value} is an invalid quality value, must be between 1 and 10.")
    return ivalue

def check_ratio_range(value):
    """
    检查输入的截图组合宽高比格式是否为"4:5"。
    
    :param value: 输入的截图组合宽高比格式
    :return: 如果截图组合宽高比格式正确，则返回该值的列表；否则抛出异常
    """
    ivalue = value.split(':')
    if len(ivalue) != 2 or not ivalue[0].isdigit() or not ivalue[1].isdigit():
        raise argparse.ArgumentTypeError(f"{value} is an invalid ratio value, must be in the format '4:5'.")
    # 宽高比相乘不超过40
    if int(ivalue[0]) * int(ivalue[1]) > 40:
        raise argparse.ArgumentTypeError(f"{value} is an invalid ratio value, the product of the two numbers cannot exceed 40.")
    
    return ivalue


def combine_frame(frame_dict, ratio, info):
    width, height = info['resolution']
    # 将所有图像按顺序存储到列表中
    images = list(frame_dict.values())
    
    # 创建一个新的空白图像，大小为4x5的组合
    combined_image = Image.new('RGB', (width * int(ratio[1]), height * int(ratio[0])))
    
    # 将字典中的图像按顺序放入组合图像中
    for idx, (key, image) in enumerate(frame_dict.items()):
        x = (idx % int(ratio[1])) * width
        y = (idx // int(ratio[1])) * height
        combined_image.paste(image, (x, y))

        
    return combined_image
    
    


# 参数解析
def parser():
    parser = argparse.ArgumentParser(description="从视频文件中获取指定时间点的截图")
    parser.add_argument('video', help="视频文件路径，可以拖入视频文件")
    # parser.add_argument('time', nargs='?', default=5.0, type=float, help="截图时间点（秒数）")
    # 截图质量
    parser.add_argument('-q', '--quality', nargs='?', default=5 , type=check_quality_range, help="截图质量，可选值1~9，默认为5")
    # 截图宽高比
    parser.add_argument('-r', '--ratio', nargs='?', default='4:5', type=check_ratio_range, help="截图组合宽高比，默认为4:5")
    # 是否跳过头尾
    parser.add_argument('-s', '--skip', action='store_true', help="是否跳过头尾，默认为False")
    # 输出图像文件路径
    parser.add_argument('-o', '--output', nargs='?', default='screenshot.jpg', help="输出图像文件路径，默认为screenshot.jpg")
    
    args = parser.parse_args()
    return args
    
    # def error(self, message):
    #     print(f"错误：{message}")
    #     self.print_help()
    #     exit(2)

def main():
    args = parser()
    
    video_info = get_video_info(args.video)
    screenshot_dict = {}
    num = int(args.ratio[0])*int(args.ratio[1]) + 1 
    parts = [video_info['duration'] / num] * num
    for i, part in enumerate(parts):
        # print(f'{i}.jpg', part*i)
        if i == 0: continue
        # 加入字典
        screenshot_dict[i] = capture_frame(args.video, f'img/{i}.jpg', round(part*(i), 3))
    
    screenshot_dict[1].save('image.png')
        
    combine_frame(screenshot_dict, args.ratio, video_info).save(args.output)

    # capture_frame(args.video, args.output, args.time)
    print(video_info)
    print(args)

# 示例使用
video = 'video/video.mp4'
output = 'img/screenshot.jpg'
time = 5  # 截取视频90秒时的帧

# python test.py 'video/video.mp4' 5 -q 9
# python test.py 'video/video.mp4' 5 -q 9 -r 16:9

if __name__ == '__main__':
    main()

# nuitka --mingw64 --standalone --show-memory --lto=no --assume-yes-for-downloads
# --output-dir=build --disable-console test.py
#python -m nuitka --mingw64 --show-memory --output-dir=build --windows-console-mode=disable --standalone --lto=no  --onefile main.py

