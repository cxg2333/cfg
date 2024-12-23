
import torch
from config import ALPHA, BETA, GAMMA, THETA

def phi(I, i, j):
    """
    计算重心函数 Φ(I, i, j)
    :param I: 输入张量，形状为 [4, 3, 224, 224]
    :param i: x 的幂次
    :param j: y 的幂次
    :return: 计算结果
    """
    # 获取张量的形状
    batch_size, channels, height, width = I.shape
    
    # 创建网格坐标
    x = torch.arange(width).view(1, 1, 1, width).expand(batch_size, channels, height, width).float()
    y = torch.arange(height).view(1, 1, height, 1).expand(batch_size, channels, height, width).float()
    
    # 计算 Φ(I, i, j)
    return (I * (x ** i) * (y ** j)).sum(dim=(2, 3))

def l1_distance(a, b):
    """
    计算 L1 距离
    :param a: 第一个张量
    :param b: 第二个张量
    :return: L1 距离
    """
    return torch.abs(a - b).sum()

def pixel_loss(S, C):
    """
    计算两个张量之间的L1损失。
    
    参数:
    S (torch.Tensor): 输入张量
    C (torch.Tensor): 目标张量
    
    返回:
    torch.Tensor: L1损失值
    """
    # 计算L1距离
    return l1_distance(S,C)

import torch

def overlap_loss(S):
    """
    计算一个张量的重叠损失。
    
    参数:
    S (torch.Tensor): 输入张量

    返回:
    torch.float32: 损失值
    """
    S_minus_one = S - 1
    max_part = torch.clamp(S_minus_one, min=0)
    min_part = torch.clamp(max_part, max=1)
    # 分子
    numerator = torch.sum(min_part)
    # 分母
    denominator = torch.sum(S)
    if denominator == 0:
        return torch.tensor(0.0)
    L_overlap = numerator / denominator
    
    return L_overlap

def centroid_loss(S, C):
    """
    计算重心损失 Lcent
    :param S: 合成字符张量，形状为 [4, 3, 224, 224]
    :param C: 真实字符张量，形状为 [4, 3, 224, 224]
    :return: 重心损失 Lcent
    """
    # 计算 Φ(S, 1, 0) 和 Φ(C, 1, 0)
    phi_S_1_0 = phi(S, 1, 0)
    phi_C_1_0 = phi(C, 1, 0)
    
    # 计算 Φ(S, 0, 1) 和 Φ(C, 0, 1)
    phi_S_0_1 = phi(S, 0, 1)
    phi_C_0_1 = phi(C, 0, 1)
    
    # 计算 L1 距离
    distance_1 = l1_distance(phi_S_1_0 / phi(S, 0, 0), phi_C_1_0 / phi(C, 0, 0))
    distance_2 = l1_distance(phi_S_0_1 / phi(S, 0, 0), phi_C_0_1 / phi(C, 0, 0))
    
    # 计算重心损失 Lcent
    Lcent = 0.5 * (distance_1 + distance_2)
    
    return Lcent



def inertia(S, C):
    """
    计算合成字符 S 和真实字符 C 之间的惯性损失（L_inertia）。
    
    该损失函数通过计算合成字符和真实字符的二阶中心矩（惯性矩）来确保每个像素到质心的距离相同。
    
    参数:
    S -- 合成字符的图像数据
    C -- 真实字符的图像数据
    
    返回:
    L_inertia -- 合成字符和真实字符之间的惯性损失
    """
    phi_S = phi(S, 2, 0) - (phi(S, 1, 0) ** 2) / phi(S, 0, 0) + phi(S, 0, 2) - (phi(S, 0, 1) ** 2) / phi(S, 0, 0)
    phi_C = phi(C, 2, 0) - (phi(C, 1, 0) ** 2) / phi(C, 0, 0) + phi(C, 0, 2) - (phi(C, 0, 1) ** 2) / phi(C, 0, 0)
    
    loss = l1_distance(phi_S, phi_C)
    
    return loss

def total_loss(S,C):
    """
    计算总损失 L = αLpixel + βLoverlap + γLcent + θLinertia
    
    参数:
    S -- 合成字符的图像数据
    C -- 真实字符的图像数据
    
    返回:
    总损失值
    """
    L_pixel = pixel_loss(S, C)
    L_overlap = overlap_loss(S)
    L_cent = centroid_loss(S, C)
    L_inertia = inertia(S, C)

    total_loss = (ALPHA * L_pixel + 
                    BETA * L_overlap + 
                    GAMMA * L_cent + 
                    THETA * L_inertia)
    
    return total_loss