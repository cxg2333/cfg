### 删掉全黑的图片，便于将数据集合并
import os
from PIL import Image

def is_black_image(image_path):
    """检查图片是否为全黑"""
    with Image.open(image_path) as img:
        # 将图片转换为RGB模式
        img = img.convert('RGB')
        # 获取图片的像素数据
        pixels = img.getdata()
        # 检查每个像素是否都是黑色
        for pixel in pixels:
            if pixel != (0, 0, 0):  # RGB值为(0, 0, 0)表示黑色
                return False
    return True

def main():
    input_folder = 'path/to/save/images/MiSans-L3'  # 替换为你的输入文件夹路径
    num = 0

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):  # 根据需要添加其他格式
            image_path = os.path.join(input_folder, filename)
            if is_black_image(image_path):
                # 如果是全黑图片，删除它
                os.remove(image_path)
                num+=1
    print(f"删掉了{num}个字")

if __name__ == '__main__':
    main()
