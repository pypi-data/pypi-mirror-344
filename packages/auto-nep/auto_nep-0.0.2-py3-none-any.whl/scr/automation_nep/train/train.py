#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：automation_nep
@File ：train.py
@Author ：RongYi
@Date ：2025/4/29 14:19
@E-mail ：2071914258@qq.com
"""

from utils.myprint import myprint
from dataset.abacus import abacus_dataset
from dataset.nep import abacus2xyz
from utils.task import sub_task, check_task
from train.nep import train_nep_v0


def train(config):
    """
    训练逻辑实现 分为 abacus gpumd nep 三个板块
    :param env_dict:
    :param config:
    :return:
    """
    if config['task_type'] == 'abacus':
        myprint("abacus 单点能计算开始")
        dataset_roots = abacus_dataset(config)  # 生成数据集 返回数据集大小
        sub_task(config, dataset_roots)  # 提交任务
        check_task(config, dataset_roots)  # 任务监测
        abacus2xyz(config["abacus"]["dataset_path"])  # 单点能提取
        train_nep_v0(config)  # nep-v0 训练
