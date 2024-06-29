import cv2
from PIL import Image, ImageDraw, ImageFont
import argparse


def capture_frame(video_path, time):
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

    cap.release()
    # 将OpenCV的BGR图像转换为RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 100)

    # 添加文字水印
    draw.text((10, 10), str(time), font=font, fill=(255, 255, 255, 128))  # 使用白色半透明文字

    return image


def get_video_info(video_path):
    """
    获取视频文件信息，包括文件大小、视频分辨率和时长。

    :param video_path: 视频文件路径
    :return: 包含视频信息的字典
    """
    cap = cv2.VideoCapture(video_path)
    # 检查视频是否成功打开
    if not cap.isOpened():
        raise ValueError("无法打开视频文件")
    # 获取视频的帧率
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 获取视频的总帧数
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 获取视频的时长（秒）
    duration = round(frame_count / fps, 3)

    # 获取视频的分辨率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cap.release()
    video_info = {
        "resolution": (width, height),
        "duration": duration
    }

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
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid ratio value, the product of the two numbers cannot exceed 40.")

    return ivalue


def combine_frame(frame_list, ratio, info):
    width, height = info['resolution']

    # 创建一个新的空白图像，大小为4x5的组合
    combined_image = Image.new('RGB', (width * int(ratio[1]), height * int(ratio[0])))

    # 将字典中的图像按顺序放入组合图像中
    for idx, image in enumerate(frame_list):
        x = (idx % int(ratio[1])) * width
        y = (idx // int(ratio[1])) * height
        combined_image.paste(image, (x, y))

    return combined_image


# 参数解析
def parser():
    parser = argparse.ArgumentParser(description="从视频文件中获取指定时间点的截图")
    parser.add_argument('video', help="视频文件路径，可以拖入视频文件")
    # 截图质量
    parser.add_argument('-q', '--quality', nargs='?', default=5, type=check_quality_range,
                        help="截图质量，可选值1~9，默认为5")
    # 截图宽高比
    parser.add_argument('-r', '--ratio', nargs='?', default='4:5', type=check_ratio_range,
                        help="截图组合宽高比，默认为4:5")
    # 是否跳过头尾
    parser.add_argument('-s', '--skip', action='store_true', help="是否跳过头尾，默认为False")
    # 输出图像文件路径
    parser.add_argument('-o', '--output', nargs='?', default='screenshot.jpg',
                        help="输出图像文件路径，默认为screenshot.jpg")

    args = parser.parse_args()
    return args


def main():
    args = parser()

    video_info = get_video_info(args.video)
    screenshot_list = []
    num = int(args.ratio[0]) * int(args.ratio[1]) + 1
    if args.skip:
        parts = [(video_info['duration'] - 180) / num] * num
    else:
        parts = [video_info['duration'] / num] * num
    for i, part in enumerate(parts):
        # if i == 0:
        #     continue
        # 加入列表
        if args.skip:
            screenshot_list.append(capture_frame(args.video, round(part * i+90, 3)))
        elif i == 0:
            continue
        else:
            screenshot_list.append(capture_frame(args.video, round(part * i, 3)))

    # screenshot_dict[1].save('image.png')

    combine_frame(screenshot_list, args.ratio, video_info).save(args.output)

    # print(video_info)
    # print(args)


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

# python -m nuitka --mingw64 --standalone --show-memory --follow-imports --lto=no
# --assume-yes-for-downloads --output-dir=build --disable-console --onefile main.py
