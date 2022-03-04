#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time     : 2022-03-01 11:00
# @Author   : codehorse
# @FileName : slow_log_parse_1.py
# @description : mysql slowlog parse
# @email    : xxxxxxxxxxxxx


import time
import xlwt
import re
import pandas as pd
import matplotlib.pyplot as plt

class SlowSqlParse(object):
    def __init__(self,slow_logfile,slow_logfile_text,excel_name):
        self.slow_logfile = slow_logfile
        self.excel_name = excel_name
        self.slow_logfile_text = slow_logfile_text

    # 设置excel表样式
    def set_style(self):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.color_index = 4
        font.height = 280
        style.font = font
        return style

    # 分析慢sql日志并写入excel表
    def write_excel(self):
        f = xlwt.Workbook()
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        excel_name = self.excel_name + '_' + nowtime + '.xls'
        sheet1 = f.add_sheet(u'慢查询SQL语句', cell_overwrite_ok=True)
        row0 = [u'提供时间', u'计数总和', u'执行时长(秒)', u'慢查询SQL语句', u'是否解决', u'备注原因']
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i], self.set_style())
        # 以下处理慢SQL文件
        fp = open(self.slow_logfile, 'r')
        fp_t = open(self.slow_logfile_text, 'w')
        for eachLine in fp.readlines():
            fp_t.write(eachLine.replace("\n", ' '))
        fp_t.close()
        fp.close()
        files = open(self.slow_logfile_text, 'r')
        text = files.read()
        # 根据关键字进行切割，
        m = text.split("Count:")
        print(m)
        if m is not None:
            size = int(len(m))
            for j in range(size):
                if j != 0:
                    countNum = re.findall(r"(.*)Time", m[j])
                    times = re.findall(r"Time=(\d+\.?\d*)", m[j])
                    sqls = re.findall(r"SELECT.*|SELECT .*|select .*|select.*|CALL .*|call .*|create .*|CREATE .*|insert .*|INSERT .*|delete *|DELETE .*|update .*|UPDATE .*", m[j])
                    if len(countNum) != 0 and len(times) != 0 and len(sqls) != 0:
                        sheet1.write(j, 0, nowtime, self.set_style())
                        sheet1.write(j, 1, countNum, self.set_style())
                        sheet1.write(j, 2, times, self.set_style())
                        sheet1.write(j, 3, sqls, self.set_style())
        files.close()
        f.save(excel_name)

    # 慢sql可视化
    def slow_sql_parse(self):
        fp = open(self.slow_logfile, 'r')
        fp_t = open(self.slow_logfile_text, 'w')
        for eachLine in fp.readlines():
            fp_t.write(eachLine.replace("\n", ' '))
        fp_t.close()
        fp.close()
        files = open(self.slow_logfile_text, 'r')
        text = files.read()
        # 根据关键字进行切割，
        m = text.split("Count:")
        slow_sql = []
        exec_time = []
        if m is not None:
            size = int(len(m))
            for j in range(size):
                if j != 0:
                    times = re.findall(r"Time=(\d+\.?\d*)", m[j])
                    sqls = re.findall(r"SELECT.*|SELECT .*|select .*|select.*|CALL .*|call .*|create .*|CREATE .*|insert .*|INSERT .*|delete *|DELETE .*|update .*|UPDATE .*", m[j])
                    if len(times) != 0 and len(sqls) != 0:
                        tmp_list = []
                        tmp_list.append(sqls[0].strip(' ').strip('\n').split(' ')[0])
                        tmp_list.append(sqls[0].strip(' ').strip('\n').split(' ')[1])
                        slow_sql.append(' '.join(tmp_list) + '...')
                        exec_time.append(float(times[0].strip(' ').strip('\n')))
        files.close()
        data = {
            'slow_sql':slow_sql,
            'exec_time':exec_time
        }
        df = pd.DataFrame(data=data)
        # 绘图
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['font.size'] = 8
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(12, 5))
        plt.xticks(rotation=20)
        plt.bar(df['slow_sql'], df['exec_time'], color='green', width=0.3, label='慢sql执行时间图')
        plt.title('慢sql执行时间图')
        plt.legend()
        plt.xlabel('sql语句')
        plt.ylabel('执行时间(单位：秒)')
        plt.show()

if __name__ == '__main__':
    obj = SlowSqlParse('slow.log','tmpfile.txt','慢SQL语句')
    obj.write_excel()
    obj.slow_sql_parse()
