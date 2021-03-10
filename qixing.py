# coding:utf-8

import requests
import xlrd
import xlsxwriter
import re
from bs4 import BeautifulSoup
import time


# 通过期数获取奖码
def get_lottery_by_id(lottery_id):
    lottery_id = str(lottery_id)
    url = "http://kaijiang.500.com/shtml/qxc/" + lottery_id + ".shtml"
    if lottery_id == "latest":
        url = "http://kaijiang.500.com/shtml/qxc/"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    if response.status_code == 404:
        return
    doc = response.text
    soup = BeautifulSoup(doc, "lxml")
    award_code = [lottery_id, "0"]
    for div in soup.find_all('li', class_='ball_orange'):
        award_code.append(div.text)

    if award_code[2].isdigit():
        award_code[1] = int(award_code[2]) + int(award_code[3]) + int(award_code[4]) + int(award_code[5])

    return award_code


def get_lottery_num(periods=60, get_num=True):
    periods -= 1
    data_list = []
    response = requests.get("http://kaijiang.500.com/shtml/qxc/")
    response.encoding = response.apparent_encoding
    doc = response.text
    soup = BeautifulSoup(doc, "lxml")
    per_str = soup.find_all(class_='iSelectList')
    latest_str = soup.find_all(class_='cfont2')
    latest_num = re.findall(r'<strong>(.*?)</strong>', str(latest_str), re.DOTALL)[0]

    ptr = r'.shtml">(.*?)</a>'
    # 获取往期列表
    per_list = re.findall(ptr, str(per_str[0].__str__), re.DOTALL)

    # 如果get_num为False，返回往期列表
    if not get_num:
        return per_list[periods::-1]

    for pr in per_list[periods::-1]:
        data_list.append(get_lottery_by_id(pr))

    # 判断是否最新一期
    if latest_num != per_list[0]:
        award_code = [latest_num, "0"]
        for div in soup.find_all('li', class_='ball_orange'):
            award_code.append(div.text)
        award_code[1] = int(award_code[2]) + int(award_code[3]) + int(award_code[4]) + int(award_code[5])
        data_list.append(award_code)

    return data_list


# 设置最后一列，周期为cycle
def per(star_list, cycle=7):
    num = 1
    k = 1
    for row in star_list[::-1]:
        if num == cycle:
            num = str(num) + str(k)
            row.append(num)
            k = k + 1
            num = 1
        else:
            row.append(num)
            num = num + 1
    return star_list


def data2excel(star_list):
    # 新建一个excel表
    fh1 = xlsxwriter.Workbook("./qxc.xlsx")

    # 新建一个sheet表
    new_sheet = fh1.add_worksheet()

    # 设置列宽度
    new_sheet.set_column("C:F", 7.56)
    new_sheet.set_column("A:A", 7.56)
    new_sheet.set_column("B:B", 5)
    new_sheet.set_column("G:I", 5)

    # 行背景标志
    odd = True

    for i in range(len(star_list) + 1):
        default_format = {
            'bold': True,  # 加粗
            'top': 0,
            'bottom': 0,
            'left': 1,
            'right': 1,
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'fg_color': '#FFFF',  # 颜色填充
            'text_wrap': True,  # 是否自动换行
        }

        # 设置行高
        new_sheet.set_row(i, 31.5)
        default_format['font_name'] = 'Times New Roman'

        # 设置框架底部颜色
        if i % 4 == 0:
            default_format['bottom_color'] = 'red'
            default_format['bottom'] = 5

        # 行背景
        if odd:
            default_format['fg_color'] = '#E6E8FA'
            odd = False
        else:
            odd = True
        for j in range(len(star_list[2])):
            # 字体大小和颜色
            if 1 < j < 6:
                default_format['font_size'] = 25
            elif j == 0:
                default_format['font_size'] = 10
            else:
                default_format['font_size'] = 15

            if j == 9:
                default_format['font_color'] = 'red'
            else:
                default_format['font_color'] = 'black'
            # 写入
            normal_format = fh1.add_format(default_format)
            # 最后一行空行
            if i == len(star_list):
                new_sheet.write(i, j, "", normal_format)
                continue
            new_sheet.write(i, j, star_list[i][j], normal_format)
            default_format['font_size'] = 15
            normal_format = fh1.add_format(default_format)
            # 设置第二列的公式
            if star_list[i][2].isdigit():
                new_sheet.write_formula(i, 1, '=C' + str(i + 1) + '+D' + str(i + 1) + '+E' +
                                        str(i + 1) + '+F' + str(i + 1), normal_format)
    # 关闭该excel表
    fh1.close()


if __name__ == "__main__":
    data = get_lottery_num(1)
    print(per(data, 7))
