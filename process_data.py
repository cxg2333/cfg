import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split
from build_dataset.build_trainset import CharacterDataset
from vgg_model.feature_process_pipline import FeatureProcessingPipeline
from utils import transform_process
from loss_def import total_loss
from tqdm import tqdm
import numpy as np


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class CharacterModelExcuter:
    def __init__(self, txt_file, image_dir, model_save_path, batch_size, epochs, learning_rate):
        self.txt_file = txt_file
        self.image_dir = image_dir
        self.model_save_path = model_save_path
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate

        
        # 创建数据集
        self.transform = transform_process()
        self.dataset = CharacterDataset(txt_file=self.txt_file, image_dir=self.image_dir, transform=self.transform)

        # 划分训练集和测试集
        train_size = int(0.8 * len(self.dataset))  # 80% 作为训练集
        test_size = len(self.dataset) - train_size  # 剩余 20% 作为测试集
        self.train_dataset, self.test_dataset = random_split(self.dataset, [train_size, test_size])

        # 创建数据加载器
        self.train_loader = DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)
        self.test_loader = DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False)

        # 初始化特征处理管道
        self.feature_pipeline = FeatureProcessingPipeline()

        # 初始化模型和优化器
        self.model = self.initialize_model()  # 假设你有一个初始化模型的方法
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def initialize_model(self):
        return FeatureProcessingPipeline()

    def apply_affine_transform(self, images, affine_matrices):
        """
        对输入图像应用仿射变换。

        参数:
        images: 输入图像，形状为 (batch_size, channels, height, width)
        affine_matrices: 仿射矩阵，形状为 (batch_size, 2, 3)

        返回:
        变换后的图像，形状与输入图像相同
        """
        # 获取 batch_size
        batch_size = images.size(0)

        # 将仿射矩阵转换为适合 affine_grid 的格式
        # affine_matrices 需要是 (batch_size, 2, 3) 的形状
        # 需要将其转换为 (batch_size, 2, 3) 的形状
        affine_matrices = affine_matrices.view(batch_size, 2, 3)

        # 生成网格
        grid = F.affine_grid(affine_matrices, images.size(), align_corners=False)

        # 使用 grid_sample 进行采样
        transformed_images = F.grid_sample(images, grid, align_corners=False)

        return transformed_images

    def train(self):
        for epoch in range(self.epochs):
            tqdm.write(f'epoch/all_epochs: {epoch+1}/{self.epochs}')
            self.model.train()  # 设置模型为训练模式

            epoch_loss = 0  # 初始化每个 epoch 的损失
            for full_images, first_images, second_images in tqdm(self.train_loader):
                full_images = full_images.to(device)
                first_images = first_images.to(device)
                second_images = second_images.to(device)
                # print(full_images.shape)
                output1, output2 = self.feature_pipeline.forward(first_images, second_images)
                # print(output1.shape)
                # print(output2.shape)

                transformed_first_images = self.apply_affine_transform(first_images, output1)
                transformed_second_images = self.apply_affine_transform(second_images, output2)
                # print(transformed_first_images.shape)
                # print(transformed_second_images.shape)

                generated_images = transformed_first_images + transformed_second_images

                loss = total_loss(generated_images, full_images)

                # 反向传播和优化
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item()  # 累加损失

            # 计算并打印每个 epoch 的平均损失
            avg_loss = epoch_loss / len(self.train_loader)
            print(f'Epoch [{epoch+1}/{self.epochs}], Average Loss: {avg_loss:.4f}')

            # 保存模型
            self.save_model(epoch)


    def predict(self, input_images):
        self.model.eval()  # 设置模型为评估模式
        with torch.no_grad():  # 不计算梯度
            output1, output2 = self.feature_pipeline.process_images(input_images[0], input_images[1])
            transformed_first_images = self.apply_affine_transform(input_images[0], output1)
            transformed_second_images = self.apply_affine_transform(input_images[1], output2)
            generated_images = transformed_first_images + transformed_second_images
        return generated_images

    def save_model(self, epoch):
        model_path = os.path.join(self.model_save_path, f'model_epoch_{epoch+1}.pth')
        torch.save(self.model.state_dict(), model_path)
        print(f'Model saved to {model_path}')

