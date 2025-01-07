# -*- coding: utf-8 -*-
# @Time : 2024/10/2 下午10:55
# @Author : D.N. Huang
# @Email : CarlCypress01@gmail.com
# @File : demo.py
# @Project : fitness_evaluation

import os
from c2net.context import prepare
from fitness_evaluation.calculation import predict


action_type = 1  # 运动类型，解释参考README.md
# 指定推理数据集和模型路径
c2net_context = prepare()
video_path = os.path.join(c2net_context.dataset_path, 'Fitness_video', 'Fitness_video')
model_path = os.path.join(c2net_context.pretrain_model_path, 'fitness_evaluation_model_knvi')

predict(
    video_path=os.path.join(video_path, f'action{action_type}.mp4'),
    action_type=action_type,
    model_path=os.path.join(model_path, 'yolov8x-pose-p6.pt'),
    save_dir='./result'
)
