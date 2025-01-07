# -*- coding: utf-8 -*-
# @Time : 2024/10/2 下午9:35
# @Author : D.N. Huang
# @Email : CarlCypress01@gmail.com
# @File : calculation.py
# @Project : fitness_evaluation

from mindtorch.tools import mstorch_enable
from fitness_evaluation.funcs import *
from ultralytics import YOLO
import cv2
import os


def predict(
        video_path: os.path,
        action_type: int,
        model_path: os.path,
        save_dir='./result',
        progress=True
):
    """
    对视频动作进行评分。
    Args:
        video_path: 需要进行评估的视频路径
        action_type: 视频对应的动作类型
        model_path: 进行关键点识别的模型路径
        save_dir: 评估视频的保存路径
        progress: 是否打印中间得分过程
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    y_list = np.load(os.path.join(
        './fitness_evaluation/standard_data',
        f'action{action_type}.npy'
    ))
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    # 获取视频的基本信息
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 选择视频编码格式
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 获取帧率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频高度
    output_path = os.path.join(save_dir, 'evaluation.mp4')  # 本地保存路径
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = width / 1000  # 根据视频宽度动态调整字体大小
    thickness = int(width / 500)  # 根据视频宽度动态调整字体粗细
    position = (int(width * 0.01), int(height * 0.05))  # 根据分辨率动态调整文字位置

    step, score_list, improve_frames = 0, [], []
    while cap.isOpened():
        font_color = (139, 0, 0)  # 深蓝色字体
        ret, frame = cap.read()
        if not ret:
            break
        data = model(frame)
        x = data[0].keypoints.data.cpu().numpy().reshape((-1, 3))[:17, :2]
        y = y_list[step]
        aligned_x, aligned_y = align_two_sets(x, y)
        angles_x = calculate_all_angles(aligned_x)
        angles_y = calculate_all_angles(aligned_y)
        vector_x = unify_data_to_vector(aligned_x, angles_x)
        vector_y = unify_data_to_vector(aligned_y, angles_y)
        cos = calculate_cosine_similarity(vector_x, vector_y)

        if np.isnan(cos):
            cos = 2
        score_list.append(cos)

        if cos < 0.9:
            font_color = (0, 0, 139)  # 深蓝色字体
            text = f'Frame {step} action needs to be improved!'
            improve_frames.append(text)
            print(text)
        elif progress:
            if cos == 2:
                cos = 0.5
            text = f'The action score of Frame {step} is {cos:.2f}.'
            print(text)
        step += 1
        # 在当前帧上绘制文字
        cv2.putText(frame, text, position, font, font_scale, font_color, thickness)
        # 将修改后的帧写入输出文件
        out.write(frame)
    score_list = replace_twos_with_zero(score_list)
    score = sum(score_list) / len(score_list)
    [print(imp) for imp in improve_frames]
    print(f'The overall action score is {score:.2f}.')

    # 释放视频对象
    cap.release()
    out.release()
    pass