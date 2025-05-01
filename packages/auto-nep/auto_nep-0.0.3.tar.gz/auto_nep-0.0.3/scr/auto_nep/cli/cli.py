#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：automation_nep
@File ：cli.py
@Author ：RongYi
@Date ：2025/4/29 14:31
@E-mail ：2071914258@qq.com
"""
import argparse
from train.train import train
from utils.config import load_config

def main():
    """
    命令行参数设置
    :return:
    """
    parser = argparse.ArgumentParser(description="Automation NEP CLI")
    subparsers = parser.add_subparsers(dest="command")

    # 添加 train 子命令
    train_parser = subparsers.add_parser("train", help="Run training")
    # 为 train 添加子命令 yaml 配置文件
    train_parser.add_argument("-yaml", default="train.yaml", help="train config file")

    args = parser.parse_args()
    if args.command == 'train':
        config_path = args.yaml
        config = load_config(config_path)
        train(config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
