# import os 
# from torchvision import models
# from torchvision.models import VGG19_Weights

# save_path = "vgg_model/"

# model = models.vgg19(weights = VGG19_Weights.DEFAULT).eval()

from torchvision import models
import torch
from PIL import Image
from torchvision import transforms


weights_path = 'vgg_model/vgg19-dcbb9e9d.pth'  # 替换为您的权重文件路径

model = models.vgg19(weights=None).eval()
model.load_state_dict(torch.load(weights_path))

image = Image.open("datasets/path/to/save/images/test/阿.png").convert('L')
image = image.convert('RGB')
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

image_tensor = transform(image).unsqueeze(0)
output = model(image_tensor)
print(output.shape)
