import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models

class FeatureExtractor:
    def __init__(self):
        self.model = models.vgg19_bn(pretrained=True)
        self.model.eval()
        self.features = nn.Sequential(*list(self.model.features.children())[:38]) 

    def extract_features(self, image):

        with torch.no_grad():
            feature = self.features(image)  # 提取中间特征
        return feature

# def get_image_paths(components):
#     image_paths = []
#     for component in components:
#         image_path = f"datasets/path/to/save/images/AlibabaPuHuiTi-3-55-Regular/{component}.png"  # 假设图片命名为 '字符.png'
#         if os.path.exists(image_path):  # 检查文件是否存在
#             image_paths.append(image_path)
#     return image_paths

# with open('datasets/lr_filtered_ids.txt', 'r', encoding='utf-8') as file:
#     data = file.readlines()

# dataset = CharacterDataset(data)
# dataset.parse_data()
# dataset.split_data(train_ratio=0.8)

# # 创建特征提取器
# feature_extractor = FeatureExtractor()

# # 提取特征并进行特征融合
# for item in dataset.train_set:
#     character = item['character']
#     components = item['components']
    
#     # 获取图片路径
#     image_paths = get_image_paths(components)
    
#     # 提取每个组件的特征
#     features_list = []
    
#     # 设定一个批次大小
#     batch_size = 2  # 你可以根据需要调整这个值
#     for i in range(0, len(image_paths), batch_size):
#         batch_image_paths = image_paths[i:i + batch_size]
#         features = feature_extractor.extract_features(batch_image_paths)
#         features_list.append(features)

#     fused_features = torch.cat(features_list, dim=1)  # dim=1 表示在通道维度拼接
#     print(f"字符: {character}, 融合特征形状: {fused_features.shape}")

