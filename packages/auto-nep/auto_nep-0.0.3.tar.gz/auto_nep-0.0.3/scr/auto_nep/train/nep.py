#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：automation_nep
@File ：nep.py
@Author ：RongYi
@Date ：2025/4/30 19:35
@E-mail ：2071914258@qq.com
"""
import os


def train_nep_v0(config):
    with open("./nep-dataset/nep.in", 'w', encoding='utf-8') as f:
        element_type = config["element_type"]
        cutoff = config["nep"]["cutoff"]

        f.write(f"type {len(element_type)}")
        for ele in element_type:
            f.write(f" {ele}")

        f.write(f"\ncutoff")
        for cutoff in cutoff:
            f.write(f" {cutoff}")
    os.system(f'{config["nep"]["nep_path"]}')


