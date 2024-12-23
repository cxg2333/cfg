import torch
class FeatureFusion:
    @staticmethod
    def fuse_feature(features_list):
        # 在通道维度上拼接特征
        fused_feature = torch.cat(features_list, dim=1)
        return fused_feature