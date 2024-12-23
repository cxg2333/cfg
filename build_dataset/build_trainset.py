import os
from PIL import Image
from torch.utils.data import Dataset

class CharacterDataset(Dataset):
    def __init__(self, txt_file, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.data = self.load_data(txt_file)

    def load_data(self, txt_file):
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        data = [line.strip() for line in lines if line.strip()]
        return data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        line = self.data[idx]
        full_char = line[0] 
        first_char = line[1]
        second_char = line[2]

        # 加载图片
        full_char_image = Image.open(os.path.join(self.image_dir, f"{full_char}.png")).convert('RGB')
        first_char_image = Image.open(os.path.join(self.image_dir, f"{first_char}.png")).convert('RGB')
        second_char_image = Image.open(os.path.join(self.image_dir, f"{second_char}.png")).convert('RGB')
        
        if self.transform:
            full_char_image = self.transform(full_char_image)
            first_char_image = self.transform(first_char_image)
            second_char_image = self.transform(second_char_image)

        return full_char_image, first_char_image, second_char_image