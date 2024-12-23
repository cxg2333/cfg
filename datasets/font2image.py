### 从ttf文件中获得相应图片
import os
from ttf_utils import *
from tqdm import tqdm

def read_characters_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        characters = f.read().strip()
    return characters

char_file_path = 'char_list.txt'
char2img_list = read_characters_from_file(char_file_path)

font_file = 'path/to/save/ttf/' 
image_file = 'path/to/save/images/' 
fonts = os.listdir(font_file)

for font in fonts:
    font_path = os.path.join(font_file, font)
    print(font_path)
    try:
        font2image(font_path, image_file, char2img_list, 128)
        print(font)
    except Exception as e:
        print(e)

remove_empty_floder(image_file)