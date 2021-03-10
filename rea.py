import numpy as np
import matplotlib.pyplot as plt
import ast
from matplotlib.font_manager import FontProperties  # 字体管理器

with open("./qxc.txt", "r") as t:
    data = t.readlines()


def data2pic(data):
    # 设置汉字格式
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
    # 加str坐标轴可不按顺序
    x1 = [str(d[2]) for d in data]
    x2 = [str(d[3]) for d in data]
    x3 = [str(d[4]) for d in data]
    x4 = [str(d[5]) for d in data]
    x0 = [str(d[1]) for d in data]
    # x1 = [ast.literal_eval(d)[2] for d in data]
    # x2 = [ast.literal_eval(d)[3] for d in data]
    # x3 = [ast.literal_eval(d)[4] for d in data]
    # x4 = [ast.literal_eval(d)[5] for d in data]
    # x0 = [ast.literal_eval(d)[1] for d in data]
    y = range(0, len(x1), 1)

    plt.figure(figsize=(9, 9))
    sub1 = plt.subplot(221)  # 将窗口分成2行1列，在第1个作图，并设置背景色
    plt.title("千位", y=-0.15, fontproperties=font)
    sub2 = plt.subplot(222)  # 将窗口分成2行1列，在第2个作图
    plt.title("百位", y=-0.15, fontproperties=font)
    # sub0 = plt.subplot(233)  # 将窗口分成2行1列，在第2个作图
    # plt.title("和", y=-0.25, fontproperties=font)
    sub3 = plt.subplot(223)  # 将窗口分成2行1列，在第2个作图
    plt.title("十位", y=-0.15, fontproperties=font)
    sub4 = plt.subplot(224)  # 将窗口分成2行1列，在第2个作图
    plt.title("个位", y=-0.15, fontproperties=font)

    sub1.plot(y, x1)  # 绘制子图
    sub2.plot(y, x2)
    # sub0.plot(y, x0)
    sub3.plot(y, x3)
    sub4.plot(y, x4)
    # plt.savefig('./qxc.jpg')
    plt.show()


if __name__ == "__main__":
    data
    data2pic(data)
