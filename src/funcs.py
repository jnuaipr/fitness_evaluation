# -*- coding: utf-8 -*-
# @Time : 2024/9/2 下午8:21
# @Author : D.N. Huang
# @Email : CarlCypress01@gmail.com
# @File : calculation.py
# @Project : fitness_evaluation

import numpy as np


def centralize(points):
    center = np.mean(points, axis=0)
    return points - center


def normalize_scale(points):
    max_distance = np.max(np.linalg.norm(points - np.mean(points, axis=0), axis=1))
    return points / max_distance


def align_points(points1, points2):
    # 计算最佳旋转角度
    cov_matrix = np.dot(points1.T, points2)
    U, _, Vt = np.linalg.svd(cov_matrix)
    R = np.dot(U, Vt)

    # 对points2应用旋转
    aligned_points2 = np.dot(points2, R)

    return aligned_points2


def align_two_sets(points1, points2):
    # 中心化
    points1 = centralize(points1)
    points2 = centralize(points2)

    # 归一化尺度
    points1 = normalize_scale(points1)
    points2 = normalize_scale(points2)

    # 对齐姿势
    points2_aligned = align_points(points1, points2)

    return points1, points2_aligned


def calculate_cosine_angle(points, idx1, idx2, idx3):
    A = points[idx1]
    B = points[idx2]
    C = points[idx3]

    BA = A - B
    BC = C - B

    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)

    cos_angle = dot_product / (norm_BA * norm_BC)

    return cos_angle


def calculate_all_angles(aligned_data):
    angles = []
    # 右臂弯曲角度（右肩、右肘、右腕）
    angles.append(calculate_cosine_angle(aligned_data, 5, 7, 9))
    # 左臂弯曲角度（左肩、左肘、左腕）
    angles.append(calculate_cosine_angle(aligned_data, 6, 8, 10))
    # 右腿弯曲角度（右胯、右膝、右脚踝）
    angles.append(calculate_cosine_angle(aligned_data, 11, 13, 15))
    # 左腿弯曲角度（左胯、左膝、左脚踝）
    angles.append(calculate_cosine_angle(aligned_data, 12, 14, 16))
    # 头部与右侧角度（右肩、鼻尖、右耳）
    angles.append(calculate_cosine_angle(aligned_data, 5, 0, 3))
    # 头部与左侧角度（左肩、鼻尖、左耳）
    angles.append(calculate_cosine_angle(aligned_data, 6, 0, 4))
    # 腰部右侧弯曲角度（右肩、右胯、右膝）
    angles.append(calculate_cosine_angle(aligned_data, 5, 11, 13))
    # 腰部左侧弯曲角度（左肩、左胯、左膝）
    angles.append(calculate_cosine_angle(aligned_data, 6, 12, 14))
    # 将结果转化为 numpy 数组
    angles_array = np.array(angles)
    return angles_array


def calculate_cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    cosine_similarity = dot_product / (norm1 * norm2)

    return cosine_similarity


def unify_data_to_vector(aligned_data, angles):
    # 将 aligned_data 展开为一维向量
    flattened_aligned_data = aligned_data.flatten()

    # 将 angles 添加到 flattened_aligned_data 后面
    unified_vector = np.concatenate((flattened_aligned_data, angles))

    return unified_vector


def replace_twos_with_mean(data):
    # 过滤出不为2的元素
    non_twos = [x for x in data if x != 2]

    # 检查是否有不为2的元素
    if len(non_twos) == 0:
        raise ValueError("List does not contain any elements other than 2.")

    # 计算不为2元素的均值
    mean_value = sum(non_twos) / len(non_twos)

    # 替换列表中的2
    replaced_data = [mean_value if x == 2 else x for x in data]

    return replaced_data


def replace_twos_with_zero(data):
    replaced_data = [0 if x == 2 else x for x in data]
    return replaced_data
