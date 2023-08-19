#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

from runstats import Statistics


def get_updated_stat(run_stat, new_data=None, mode='std'):
    """
    获取在线数据的统计值
    :param run_stat: 统计器，Statistics 类对象
    :param new_data: 默认为None时，获取run_stat统计器中的统计值；当不为None时，统计器先加入（push）相应数据，再返回更新后统计值
    :param mode: 统计值的类型。std代表标准差；var代表方差；mean代码均值
    :return: 更新后的统计值
    """
    if new_data is not None:
        for element in new_data:
            run_stat.push(element)
    if mode == 'std':
        return run_stat.stddev(0)
    elif mode == 'var':
        return run_stat.variance(0)
    elif mode == 'mean':
        return run_stat.mean()
    else:
        raise ValueError(f'函数 get_updated_stat 不支持 {mode}')


if __name__ == '__main__':
    stats = Statistics()
    n = 10000
    data = np.random.random((n,))
    print(np.std(data), np.var(data), np.mean(data))
    print(get_updated_stat(stats, data, mode='std'))
    print(get_updated_stat(stats, mode='var'))
    print(get_updated_stat(stats, mode='mean'))
    print(len(stats))
    stats.clear()
    print(len(stats))
