#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：automation_nep
@File ：sub_task.py
@Author ：RongYi
@Date ：2025/4/29 20:48
@E-mail ：2071914258@qq.com
"""
import os
import re
import time
import shutil
from colorama import Style
from utils.myprint import myprint


def sub_task(config, dataset_roots):
    """
    提交任务脚本
    :param config: 配置文件
    :return:
    """
    # 检查文件
    if not os.path.exists(config[f"abacus"]["pbs_path"]):
        myprint(f'未找到 {config["abacus"]["pbs_path"]} 请检查配置文件', 'RED')
        exit()
    if not os.path.exists(config["abacus"]["input_path"]):
        myprint(f'未找到 {config["abacus"]["input_path"]} 请检查配置文件', 'RED')
        exit()
    # 检查数据集路径
    if config["abacus"]["dataset_path"]:
        dataset_path = config["abacus"]["dataset_path"]
    else:
        dataset_path = "./abacus_dataset"

    # 提交任务: 收敛标准 time.json文件
    task_num = 0
    home_path = os.getcwd()
    for root in dataset_roots:
        if not os.path.exists('/'.join(root.split("/")[:-1]) + "/time.json"):
            os.chdir('/'.join(root.split("/")[:-1]))
            os.system('qsub abacus.pbs')
            shutil.copy(home_path + config["abacus"]["input_path"], '.')
            shutil.copy(home_path + config["abacus"]["pbs_path"], '.')
            task_num += 1
    # 提交完成后退回主目录
    os.chdir(home_path)
    myprint(f"任务提交完成 提交计算任务: {task_num}")


def spend_time(task_path):
    """
    读取当前任务所花费时间
    :param task_path: 任务路径
    :return: step time: h m s
    """
    with open(task_path + "/out.log", encoding='utf-8') as f:
        content = f.read()
        time_pattern = re.compile(r" CU\d+\s+.*\s+(\d+\.\d+)$", re.MULTILINE)
        time_match = time_pattern.findall(content)
        spend_time = 0
        for time in time_match:
            spend_time += float(time)
        step_pattern = re.compile(r" CU\d+\s+.*\s+\d+\.\d+$", re.MULTILINE)
        step_match = step_pattern.findall(content)
        return step_match[-1], str(int(spend_time // 3600)), str(int(spend_time // 60 % 60)), str(round(spend_time % 60))


def check_task(config, dataset_roots):
    """
    检测任务是否完成
    1.有 out.log 无 time.json 计算中
    2.有 time.json 计算完成
    3. 无 out.log 无 time.json 等待中
    :return:
    """
    start_time = time.perf_counter()
    total_time = 0  # 计算总耗时 min

    # 检查数据集路径
    if config["abacus"]["dataset_path"]:
        dataset_path = config["abacus"]["dataset_path"]
    else:
        dataset_path = "./abacus_dataset"
    # 处理未计算任务
    warn_times = 1
    while True:
        accomplish = []
        calculating = []
        awating = []
        for root in dataset_roots:
            time_json = '/'.join(root.split("/")[:-1]) + "/time.json"
            out_log = '/'.join(root.split("/")[:-1]) + f"/out.log"
            if os.path.isfile(time_json):
                accomplish.append('/'.join(root.split("/")[:-1]))
            elif os.path.isfile(out_log):
                calculating.append('/'.join(root.split("/")[:-1]))
            else:
                awating.append('/'.join(root.split("/")[:-1]))

        if total_time % 5 == 0:
            # Current Task 打印模块
            myprint("\n-------------------------------- abacus -------------------------------\n"
                   f"Total task num: {len(dataset_roots)}\t Total time(s): {round(time.perf_counter() - start_time, 2)}\t  Progress:{len(accomplish)}/{len(dataset_roots)}\n"
                   f"-----------------------------------------------------------------------")
            for task in calculating:
                step, h, m, s = spend_time(task)
                print(f"Current Task: [{task}] Spend Time: [{h}h {m}m {s}s]\n"
                      f"Step: [{step}]\n"
                      f"-----------------------------------------------------------------------")

        if len(accomplish) == len(dataset_roots):
            myprint("计算完成提取 nep 训练集 train.xyz", 'RED')
            myprint(f"Mean time(s):{(time.perf_counter() - start_time)/len(accomplish): .2f} s")
            break

        if len(calculating) == 0 and len(awating) > 0:
            myprint(f"Warning {warn_times}: 以下任务未进行计算!", "RED")
            for task in awating:
                print(f"{task + Style.RESET_ALL}")
            warn_times += 1
            if warn_times > config["abacus"]["warn_times"]:
                # 警告超过三次 自动退出 进行下一步
                break

        total_time += 1
        time.sleep(60)

