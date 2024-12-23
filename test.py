from vgg_model.feature_extractor import FeatureExtractor
from PIL import Image
import torchvision.transforms as transforms

import torchvision.models as models

# 加载 VGG19-BN 模型
vgg19_bn = models.vgg19_bn(pretrained=True)

# 打印每一层
for name, layer in vgg19_bn.named_children():
    print(f"{name}: {layer}")
# def main():
#     data_path = 'datasets/path/to/save/images/AlibabaPuHuiTi-3-55-Regular/一.png'
#     img = Image.open(data_path).convert('RGB')
#     transform = transforms.Compose([
#         transforms.Resize((224, 224)),  # VGG19 输入大小为 224x224
#         transforms.ToTensor(),           # 转换为 Tensor
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 归一化
#     ])
#     img_tensor=  transform(img).unsqueeze(0)
#     fe = FeatureExtractor()
#     feature = fe.extract_features(img_tensor)
#     print(feature.shape)

# if __name__ == '__main__':
#     main()
    