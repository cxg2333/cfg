### 删掉与对比图片相同的图片，便于将数据集合并
import os
from PIL import Image

def images_are_equal(img1_path, img2_path):
    """比较两张图片是否完全相同"""
    with Image.open(img1_path) as img1, Image.open(img2_path) as img2:
        return list(img1.getdata()) == list(img2.getdata())

def main():
    target_image_path = 'path/to/save/images/test/③.png'  # 替换为您的目标图片路径
    folder_path = 'path/to/save/images/KaiXinSongB'  # 替换为您的文件夹路径
    sum=0
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            if images_are_equal(target_image_path, image_path):
                # 如果图片相同，删除它
                os.remove(image_path)
                sum+=1
    print(f"删掉了{sum}个字")

if __name__ == '__main__':
    main()
