# -*- coding: utf-8 -*-
# @Time    : 18 1月 2025 11:34 下午
# @Author  : codervibe
# @File    : dictsociety.py
# @Project : pythonBasics
import argparse
import itertools
import logging
import os
import string

import colorlog

# 配置日志记录
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
)
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="生成社工密码字典")
parser.add_argument("--dict_file", type=str, default="dict.txt", help="密码字典文件路径，默认为 dict.txt")
parser.add_argument("--info_file", type=str, default="info.txt", help="个人信息文件路径，默认为 info.txt")
parser.add_argument("--password_length", type=int, default=4, help="密码长度，默认为 4")

args = parser.parse_args()


def read_info_list(info_file="info.txt"):
    """
    读取个人信息文件info.txt，并提取所有个人信息字段
    :param info_file: 个人信息文件路径，默认为 "info.txt"
    :return: 包含所有个人信息字段的列表
    """
    info_list = []
    if not os.path.exists(info_file):
        logger.error(f"文件 {info_file} 不存在")
        return info_list

    try:
        with open(info_file, "r", encoding="utf-8") as info:
            for line in info:
                # 提取每行信息的字段值，并添加到列表中
                parts = line.strip().split(":")
                if len(parts) == 2:
                    info_list.append(parts[1])
                else:
                    logger.warning(f"格式错误的行: {line.strip()}")
    except FileNotFoundError:
        logger.error(f"文件 {info_file} 未找到")
        return info_list
    except IOError as e:
        logger.error(f"读取个人信息文件时发生 I/O 错误: {e}")
        return info_list
    except UnicodeDecodeError:
        logger.error(f"无法解码文件 {info_file}，请检查编码设置")
        return info_list
    except Exception as e:
        logger.error(f"读取个人信息文件时发生未知错误: {e}")
        raise  # 重新抛出未知异常以便调用者处理
    return info_list


def create_number_list(length=3):
    """
    生成所有可能的指定长度的数字组合
    :param length: 数字组合的长度，默认为3
    :return: 包含所有指定长度数字组合的生成器
    """
    try:
        # 使用生成器表达式以减少内存占用
        numbers_generator = (''.join(p) for p in itertools.product(string.digits, repeat=length))
        return list(numbers_generator)  # 如果需要返回列表，可以在这里转换
    except ImportError as e:
        print(f"模块导入失败: {e}")
        return []
    except Exception as e:
        print(f"发生未知错误: {e}")
        return []


def create_special_list():
    """
    生成所有特殊字符的列表
    :return: 包含所有特殊字符的列表
    """
    return list(string.punctuation)


def generate_password_combinations(infolist, specal_list, password_length):
    """
    生成密码的所有可能组合
    :param infolist: 个人信息列表
    :param specal_list: 特殊字符列表
    :param password_length: 密码长度
    :return: 包含所有可能密码组合的集合
    """
    # 初始化一个集合，用于存储所有可能的组合
    combinations = set()

    # 遍历信息列表，寻找和生成所有可能的密码组合
    for a in infolist:
        # 如果当前元素的长度大于等于预设的密码长度，则直接添加到组合集中
        if len(a) >= password_length:
            combinations.add(a)
        else:
            # 计算还需要多少字符达到密码长度
            need_words = password_length - len(a)
            # 使用数字的排列组合来补充缺失的字符数，并添加到组合集中
            for b in itertools.permutations(string.digits, need_words):
                combinations.add(a + ''.join(b))

    # 遍历信息列表，尝试将两个元素拼接起来作为密码组合
    for a in infolist:
        for c in infolist:
            combined = a + c
            # 如果拼接后的长度大于等于密码长度，则添加到组合集中
            if len(combined) >= password_length:
                combinations.add(combined)

    # 遍历信息列表，尝试将两个信息元素和一个特殊字符元素拼接起来作为密码组合
    for a in infolist:
        for d in infolist:
            for e in specal_list:
                # 生成三种不同的拼接方式，以覆盖可能的密码结构
                combined1 = a + d + e
                combined2 = e + d + a
                combined3 = a + e + d
                # 如果拼接后的长度大于等于密码长度，则添加到组合集中
                if len(combined1) >= password_length:
                    combinations.add(combined1)
                if len(combined2) >= password_length:
                    combinations.add(combined2)
                if len(combined3) >= password_length:
                    combinations.add(combined3)

    # 返回所有生成的密码组合
    return combinations


def combination(dict_file="dict.txt", info_file="info.txt", password_length=4):
    """
    生成密码的所有可能组合，并将它们写入文件
    :param dict_file: 密码字典文件路径，默认为 "dict.txt"
    :param info_file: 个人信息文件路径，默认为 "info.txt"
    :param password_length: 密码长度，默认为 4
    """
    try:
        # 确保文件路径存在
        if not os.path.exists(os.path.dirname(dict_file)):
            os.makedirs(os.path.dirname(dict_file))
        if not os.path.exists(os.path.dirname(info_file)):
            os.makedirs(os.path.dirname(info_file))

        infolist = read_info_list(info_file)
        specal_list = create_special_list()

        if not infolist:
            logger.warning("个人信息列表为空，无法生成密码组合")
            return

        # 验证 password_length 是否合理
        if password_length <= 0 or password_length > len(infolist) + len(specal_list):
            logger.error(f"无效的密码长度 {password_length}")
            return

        # 使用生成器逐步生成密码组合
        def generate_combinations():
            for password in generate_password_combinations(infolist, specal_list, password_length):
                yield password

        with open(dict_file, "w", encoding="utf-8") as df:
            for password in generate_combinations():
                df.write(password + '\n')

        logger.info(f"生成的密码组合已写入文件 {dict_file}")

    except Exception as e:
        logger.error(f"发生错误: {e}")


# 执行密码生成函数
combination(dict_file=args.dict_file, info_file=args.info_file, password_length=args.password_length)
# 也可以选择执行read_info_list()来仅读取和打印个人信息
# print(read_info_list())
