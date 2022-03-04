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
from jinja2 import Environment,FileSystemLoader
import os

root_path = os.getcwd()

class SlowSqlParse(object):
    def __init__(self,slow_logfile,slowlog_html_tempalte,slowlog_html_report):
        self.slow_logfile = slow_logfile
        self.slowlog_html_report = slowlog_html_report
        self.slowlog_html_tempalte = slowlog_html_tempalte

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
        sheet1 = f.add_sheet(u'慢查询SQL语句', cell_overwrite_ok=True)
        row0 = [u'Query_Time', u'Lock_Time', u'Rows_Sent', u'Rows_Examined', u'Timestamp',u'Slow_Sql']
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i], self.set_style())
        content = ''
        log_file = open(self.slow_logfile)
        for line in log_file.readlines():
            line = line.strip('\n')
            content = content + line
        # Query_time: 28.216586  Lock_time: 0.000046 Rows_sent: 0  Rows_examined: 0SET timestamp=1646114282;call idata_3();
        # re_mysql = re.findall(
        # '.*?# Query_time: (.*?)  Lock_time: (.*?) Rows_sent: (.*?)  Rows_examined: (.*?) Rows_affected: (.*?)  Rows_read: (.*?).*?timestamp=(.*?);(.*?);',content, re.I
        # )
        total_record = re.findall('.*?# Query_time: (.*?)  Lock_time: (.*?) Rows_sent: (.*?)  Rows_examined: (\d+).*?timestamp=(.*?);(.*?);',content, re.I)
        if total_record is not None:
            for row_num in range(len(total_record)):
                if len(total_record[row_num]) != 0:
                    sheet1.write(row_num + 1, 0, total_record[row_num][0].strip(), self.set_style())
                    sheet1.write(row_num + 1, 1, total_record[row_num][1].strip(), self.set_style())
                    sheet1.write(row_num + 1, 2, total_record[row_num][2].strip(), self.set_style())
                    sheet1.write(row_num + 1, 3, total_record[row_num][3].strip(), self.set_style())
                    sheet1.write(row_num + 1, 4, total_record[row_num][4].strip(), self.set_style())
                    sheet1.write(row_num + 1, 5, total_record[row_num][5].strip(), self.set_style())
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        excel_path = root_path + '\\slowlog_archive\\excel'
        if not os.path.exists(excel_path):
            os.makedirs(excel_path)
        excel_name = excel_path + '\\慢sql语句' + nowtime + '.xls'
        f.save(excel_name)

    # 慢sql可视化
    def slow_sql_parse(self):
        content = ''
        log_file = open(self.slow_logfile)
        for line in log_file.readlines():
            line = line.strip('\n')
            content = content + line
        # Query_time: 28.216586  Lock_time: 0.000046 Rows_sent: 0  Rows_examined: 0SET timestamp=1646114282;call idata_3();
        # re_mysql = re.findall(
        # '.*?# Query_time: (.*?)  Lock_time: (.*?) Rows_sent: (.*?)  Rows_examined: (.*?) Rows_affected: (.*?)  Rows_read: (.*?).*?timestamp=(.*?);(.*?);',content, re.I
        # )
        total_record = re.findall(
            '.*?# Query_time: (.*?)  Lock_time: (.*?) Rows_sent: (.*?)  Rows_examined: (\d+).*?timestamp=(.*?);(.*?);',
            content, re.I)
        slow_sql = []
        exec_time = []
        if total_record is not None:
            for row_num in range(len(total_record)):
                if len(total_record[row_num]) != 0:
                    tmp_list = []
                    sql = total_record[row_num][5].strip().strip('\n')
                    if sql.find(' ') != -1:
                        first = sql.split(' ')[0]
                        second = sql.split(' ')[1]
                        tmp_list.append(first)
                        tmp_list.append(second)
                        slow_sql.append(' '.join(tmp_list) + '...')
                    else:
                        slow_sql.append(sql)
                    exec_time.append(float(total_record[row_num][0].strip()))
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
        # plt.show()
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        pic_path = root_path + '\\slowlog_archive\\pic'
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)
        pic_name = pic_path + '\\慢sql语句' + nowtime + '.jpg'
        plt.savefig(pic_name)
        return pic_name

    # 慢sql生成html文件
    def gen_slowlog_html(self,pic_name):
        content = ''
        log_file = open(self.slow_logfile)
        for line in log_file.readlines():
            line = line.strip('\n')
            content = content + line
        # Query_time: 28.216586  Lock_time: 0.000046 Rows_sent: 0  Rows_examined: 0SET timestamp=1646114282;call idata_3();
        # re_mysql = re.findall(
        # '.*?# Query_time: (.*?)  Lock_time: (.*?) Rows_sent: (.*?)  Rows_examined: (.*?) Rows_affected: (.*?)  Rows_read: (.*?).*?timestamp=(.*?);(.*?);',content, re.I
        # )
        total_record = re.findall(
            '.*?# Query_time: (.*?)  Lock_time: (.*?) Rows_sent: (.*?)  Rows_examined: (\d+).*?timestamp=(.*?);(.*?);',
            content, re.I)
        all_sql_info = []
        pic_info = {}
        pic_info['pic_name'] = pic_name
        if total_record is not None:
            total_record = [list(i) for i in total_record]
            for row_num in range(len(total_record)):
                if len(total_record[row_num]) != 0:
                   query_time = total_record[row_num][0].strip().strip('\n')
                   lock_time = total_record[row_num][1].strip().strip('\n')
                   rows_sent = total_record[row_num][2].strip().strip('\n')
                   rows_examined = total_record[row_num][3].strip().strip('\n')
                   timestamp = total_record[row_num][4].strip().strip('\n')
                   sql = total_record[row_num][5].strip().strip('\n')
                   sql_info = {
                       'id':row_num,
                       'query_time':query_time,
                       'lock_time':lock_time,
                       'rows_sent':rows_sent,
                       'rows_examined':rows_examined,
                       'timestamp':timestamp,
                       'sql':sql
                   }
                   all_sql_info.append(sql_info)
        env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
        template = env.get_template('slowlog_template.html')
        html_content = template.render(sql_info=all_sql_info,pic_info=pic_info)
        nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        html_path = root_path + '\\slowlog_archive\\html'
        if not os.path.exists(html_path):
            os.makedirs(html_path)
        with open(html_path + '\\' + self.slowlog_html_report + nowtime + '.html', 'wb') as f:
            f.write(html_content.encode('utf-8'))

if __name__ == '__main__':
    obj = SlowSqlParse('mysql_slow.log','slowlog_template.html','slowlog_report')
    obj.write_excel()
    pic_name = obj.slow_sql_parse()
    obj.gen_slowlog_html(pic_name)
