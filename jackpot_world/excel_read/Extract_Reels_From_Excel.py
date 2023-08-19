#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: Mingjun Wu
Date: 02/20/2020
"""


from __future__ import print_function

import os
import json
import sys

import pandas as pd


def excel2txt(params):
    """

    :param params:
    :return:
    """
    print('Converting... ...')
    excel_name = os.path.realpath(params['ExcelName'])
    sheet_names = params['SheetNames']
    sheet_range = params['SheetRange']
    out_txt = os.path.realpath(params['OutTxtName'])
    program_id = params['ProgramType']
    print('输入的EXCEL文件路径为：{}'.format(excel_name))
    print('输出的TXT文件路径为：{}'.format(out_txt))
    if not os.path.exists(excel_name):
        raise ValueError('不存在文件{}'.format(excel_name))
    if program_id == 0:
        print('为C++程序转化... ...')
    else:
        print('为python程序转化... ...')
    print('\n')
    num_sheets = len(sheet_names)
    if len(sheet_range) != num_sheets:
        print('The number of SheetNames is not equal to the number of SheetRange')
        return
    print("输入EXCEL文件需要有 {} 个sheets".format(num_sheets))
    with open(out_txt, 'w') as f_out:
        for i, sheet in enumerate(sheet_names):
            print("读取第{}个sheet: {} ... ...".format(i+1, sheet))
            s_range = sheet_range[i][2]+':'+sheet_range[i][3]
            print('列的范围为{}; 行的范围为{}:{}'.format(s_range, sheet_range[i][0], sheet_range[i][1]))
            current_sheet = pd.read_excel(excel_name, sheet_name=sheet, header=None, usecols=s_range,
                                          nrows=sheet_range[i][1])
            current_sheet = current_sheet.iloc[sheet_range[i][0]-1:sheet_range[i][1]]
            cols = current_sheet.shape[1]
            # write
            f_out.write(sheet+':\n')
            f_out.write('[\n')
            for col_id in range(cols):
                sheet_1_col = current_sheet.iloc[:, col_id]
                sheet_drop_nan = sheet_1_col.dropna()
                sheet_list = sheet_drop_nan.values.tolist()

                sheet_list = [(Ustr.encode('utf-8')).decode('utf-8') for Ustr in sheet_list]

                if program_id == 0:
                    len_sheet = len(sheet_list)
                    sheet_list.insert(0, len_sheet)
                    f_out.write(str(sheet_list).replace("'", ""))
                else:
                    f_out.write(str(sheet_list).replace("'", ""))
                f_out.write(',\n')
            f_out.write(']\n\n\n')
        print('\n')
    print('程序结束')
    return


if __name__ == '__main__':
    config_name = os.path.realpath(sys.argv[1])
    print('参数文件全路径为{}'.format(config_name))
    with open(config_name, 'r') as fin:
        params_in = json.load(fin)
    print('Check the parameters:')
    print(params_in)
    excel2txt(params_in)
