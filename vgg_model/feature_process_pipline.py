import torch
import torch.nn as nn
from .feature_extractor import FeatureExtractor
from .feature_fusion import FeatureFusion
from .regressor import LocalizationNetwork

class FeatureProcessingPipeline:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.feature_fusion = FeatureFusion()
        self.regressor1 = LocalizationNetwork()
        self.regressor2 = LocalizationNetwork()

    def forward(self, image1, image2):
        feature1 = self.feature_extractor.extract_features(image1)
        feature2 = self.feature_extractor.extract_features(image2)
        # print(f"第1个特征的形状：{feature1.shape}")
        # print(f"第2个特征的形状：{feature2.shape}")


        fused_feature = self.feature_fusion.fuse_feature([feature1, feature2])
        # print(f"融合特征的形状：{fused_feature.shape}")
        output1 = self.regressor1(fused_feature)
        output2 = self.regressor2(fused_feature)
        # print(f"第1个仿射矩阵的形状：{output1.shape}")
        # print(f"第2个仿射矩阵的形状：{output2.shape}")



        return output1, output2
    def parameters(self):
        # 返回所有子模块的参数
        return list(self.regressor1.parameters()) + list(self.regressor2.parameters())

    def train(self):
        self.regressor1.train()
        self.regressor2.train()