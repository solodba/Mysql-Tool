#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time     : 2022-02-28 10:30
# @Author   : codehoese
# @FileName : mysql_install.py
# @description : mysql install
# @email    : xxxxxxxxxxxxx

import sys
import os
import logging.config
import ConfigParser
import datetime

# 日志配置
logging.config.fileConfig('logger.conf')
logger = logging.getLogger('logger1')

# 导入配置
config = ConfigParser.ConfigParser(allow_no_value=True)
config.read('setup.conf')

# 硬件配置检查
class HardwareCheck(object):
    @staticmethod
    def os_release_check():
        cmd = 'cat /etc/centos-release'
        str = os.popen(cmd).read()
        result = str.split(' ')[-2].split('.')[0]
        if int(result) >= 7:
            logger.info('当前系统版本为：{0}，检查通过！'.format(result + '.' + str.split(' ')[-2].split('.')[1]))
        else:
            logger.info('当前系统版本为：{0}，检查失败！'.format(result + '.' + str.split(' ')[-2].split('.')[1]))
            logger.info('退出安装！')
            sys.exit(0)

    @staticmethod
    def os_memory_check():
        cmd = 'cat /proc/meminfo | head -1'
        str = os.popen(cmd).read()
        result = str.split(':')[-1].strip().strip('\n').split(' ')[0]
        if float(result)/1024/1024 > 16:
            logger.info('当前系统内存为：{0}G，检查通过！'.format(float(result)/1024/1024))
        else:
            logger.info('当前系统内存为：{0}G，检查失败！'.format(float(result)/1024/1024))
            logger.info('退出安装！')
            sys.exit(0)
    
    @staticmethod
    def os_swap_check():
        cmd1 = "swapon -s | sed -n '2p' | awk '{print $3}'"
        str1 = os.popen(cmd1).read()
        result1 = str1.strip().strip('\n')
        swap_size = float(result1)/1024/1024
        cmd2 = 'cat /proc/meminfo | head -1'
        str2 = os.popen(cmd2).read()
        result2 = str2.split(':')[-1].strip().strip('\n').split(' ')[0]
        memory_size = float(result2)/1024/1024
        if memory_size > 1 and memory_size < 2:
            if swap_size >= memory_size * 1.5:
                logger.info('当前系统swap大小为：{0}G，检查通过！'.format(swap_size))
            else:
                logger.info('当前系统swap大小为：{0}G，检查失败！'.format(swap_size))
                logger.info('退出安装！')
                sys.exit(0)
        if memory_size > 2 and memory_size < 16:
            if swap_size == 16:
                logger.info('当前系统swap大小为：{0}G，检查通过！'.format(swap_size))
            else:
                logger.info('当前系统swap大小为：{0}G，检查失败！'.format(swap_size))
                logger.info('退出安装！')
                sys.exit(0)
        if memory_size > 16:
            if swap_size >= 16:
                logger.info('当前系统swap大小为：{0}G，检查通过！'.format(swap_size))
            else:
                logger.info('当前系统swap大小为：{0}G，检查失败！'.format(swap_size))
                logger.info('退出安装！')
                sys.exit(0)

    @staticmethod
    def mysql_installdir_check():
        mysql_home = config.get('pre_mysql_install', 'mysql_home')
        cmd_1 = "df -h | grep '%s$' | awk '{print $1}'" % (mysql_home)
        result_1 = os.popen(cmd_1).read().strip('\n')
        if result_1.endswith('G'):
            if float(result_1.strip('G')) >= 100:
                logger.info('当前系统mysql安装目录为：{0}，大小：{1}，检查通过！'.format(mysql_home,result_1))
            else:
                logger.info('当前系统mysql安装目录为：{0}，大小：{1}，检查失败！'.format(mysql_home,result_1))
                logger.info('退出安装！')
                sys.exit(0)
        elif result_1.endswith('T'):
            logger.info('当前系统mysql家目录为：{0}，大小为：{1}，检查通过！'.format(mysql_home,result_1))
        elif result_1.endswith('M'):
            logger.info('当前系统mysql家目录为：{0}，大小为：{1}，检查失败！'.format(mysql_home,result_1))
            logger.info('退出安装！')
            sys.exit(0)
        else:
            logger.info('当前mysql家目录{0}大小检查不到，检查失败！'.format(mysql_home))
            logger.info('退出安装！')
            sys.exit(0)
              
        mysqldata = config.get('pre_mysql_install', 'mysqldata')
        cmd_2 = "df -h | grep '%s$' | awk '{print $1}'" % (mysqldata)
        result_2 = os.popen(cmd_2).read().strip('\n')
        if result_2.endswith('G'):
            if float(result_2.strip('G')) >= 100:
                logger.info('当前系统mysql数据目录为：{0}，大小：{1}，检查通过！'.format(mysqldata,result_2))
            else:
                logger.info('当前系统mysql数据目录为：{0}，大小：{1}，检查失败！'.format(mysqldata,result_2))
                logger.info('退出安装！')
                sys.exit(0)
        elif result_2.endswith('T'):
            logger.info('当前系统mysql数据目录为：{0}，大小为：{1}，检查通过！'.format(mysqldata,result_2))
        elif result_2.endswith('M'):
            logger.info('当前系统mysql数据目录为：{0}，大小为：{1}，检查失败！'.format(mysqldata,result_2))
            logger.info('退出安装！')
            sys.exit(0) 
        else:
            logger.info('当前mysql数据目录{0}大小检查不到，检查失败！'.format(mysqldata))
            logger.info('退出安装！')
            sys.exit(0)

        mysqlbinlog = config.get('pre_mysql_install', 'mysqlbinlog')
        cmd_3 = "df -h | grep '%s$' | awk '{print $1}'" % (mysqlbinlog)
        result_3 = os.popen(cmd_3).read().strip('\n')
        if result_3.endswith('G'):
            if float(result_3.strip('G')) >= 100:
                logger.info('当前系统mysqlbinlog目录为：{0}，大小：{1}，检查通过！'.format(mysqlbinlog,result_3))
            else:
                logger.info('当前系统mysqlbinlog目录为：{0}，大小：{1}，检查失败！'.format(mysqlbinlog,result_3))
                logger.info('退出安装！')
                sys.exit(0)
        elif result_3.endswith('T'):
            logger.info('当前系统mysqlbinlog目录为：{0}，大小为：{1}，检查通过！'.format(mysqlbinlog,result_3))
        elif result_3.endswith('M'):
            logger.info('当前系统mysqlbinlog目录为：{0}，大小为：{1}，检查失败！'.format(mysqlbinlog,result_3))
            logger.info('退出安装！')
            sys.exit(0) 
        else:
            logger.info('当前mysql二进制日志目录{0}大小检查不到，检查失败！'.format(mysqlbinlog))
            logger.info('退出安装！')
            sys.exit(0)

        mysqlbackup = config.get('pre_mysql_install', 'mysqlbackup')
        cmd_4 = "df -h | grep '%s$' | awk '{print $1}'" % (mysqlbackup)
        result_4 = os.popen(cmd_4).read().strip('\n')
        if result_4.endswith('G'):
            if float(result_4.strip('G')) >= 100:
                logger.info('当前系统mysql备份目录为：{0}，大小：{1}，检查通过！'.format(mysqlbackup,result_4))
            else:
                logger.info('当前系统mysql备份目录为：{0}，大小：{1}，检查失败！'.format(mysqlbackup,result_4))
                logger.info('退出安装！')
                sys.exit(0)
        elif result_4.endswith('T'):
            logger.info('当前系统mysql备份目录为：{0}，大小为：{1}，检查通过！'.format(mysqlbackup,result_4))
        elif result_4.endswith('M'):
            logger.info('当前系统mysql备份目录为：{0}，大小为：{1}，检查失败！'.format(mysqlbackup,result_4))
            logger.info('退出安装！')
            sys.exit(0) 
        else:
            logger.info('当前mysql备份目录{0}大小检查不到，检查失败！'.format(mysqlbackup))
            logger.info('退出安装！')
            sys.exit(0)    

class PreMysqlInstall(object):
    @staticmethod
    def stop_firewall():
        stop_firewall_cmd = 'systemctl stop firewalld.service > /dev/null 2>&1'
        disable_firewall_cmd = 'systemctl disable firewalld.service > /dev/null 2>&1'
        stop_result = os.system(stop_firewall_cmd)
        disable_result = os.system(disable_firewall_cmd)
        if stop_result == 0:
            logger.info('系统防火墙关闭成功！')
        else:
            logger.info('系统防火墙关闭失败，请检查执行命令！')
            logger.info('退出安装！')
            sys.exit(0)
        if disable_result == 0:
            logger.info('系统防火墙禁用成功！')
        else:
            logger.info('系统防火墙禁用失败，请检查执行命令！')
            logger.info('退出安装！')
            sys.exit(0)

    @staticmethod
    def stop_selinux():
        selinux_conf_file = '/etc/selinux/config'
        cp_result = os.system('cp {0} {1}.bak{2}'.format(selinux_conf_file,selinux_conf_file,
        datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
        if cp_result == 0:
            logger.info('备份{0}文件成功！'.format(selinux_conf_file))
        else:
            logger.info('备份{0}文件失败！'.format(selinux_conf_file))
            logger.info('退出安装！')
            sys.exit(0)
        try:
            with open(selinux_conf_file,'r') as f:
                res = f.readlines()
        except Exception as e:
            logger.info('{0}文件读取失败，报错信息：{1}'.format(selinux_conf_file,e))
            sys.exit(0)
        for i in range(len(res)):
            if res[i].strip('\n').upper() == 'SELINUX=ENFORCING':
                res[i] = 'SELINUX=disabled\n'
        try:
            with open(selinux_conf_file,'w') as f:
                f.writelines(res)
        except Exception as e:
            logger.info('{0}文件写入失败，报错信息：{1}'.format(selinux_conf_file,e))
            sys.exit(0)
        logger.info('{0}文件修改成功！'.format(selinux_conf_file))
        set_result = os.system('setenforce 0')
        if set_result > 1:
            logger.info('setenforce命令执行失败！')
        else:
            logger.info('setenforce命令执行成功！')

    @staticmethod
    def modify_host():
        host_profile = '/etc/hosts'
        ip = config.get('pre_mysql_install','ip')
        hostname = config.get('pre_mysql_install','hostname')
        host_str = '''
##############For DB#################
{0} {1}
##############End for DB#############\n'''.format(ip,hostname)
        if os.path.exists(host_profile):
            cp_result = os.system('cp {0} {1}.bak{2}'.format(host_profile,host_profile,
            datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if cp_result == 0:
                logger.info('备份{0}文件成功！'.format(host_profile))
            else:
                logger.info('备份{0}文件失败！'.format(host_profile))
                logger.info('退出安装！')
                sys.exit(0)
        else:
            logger.info('{0}文件不存在，cp备份该文件失败！'.format(host_profile))
            logger.info('退出安装！')
            sys.exit(0)
        try:
            with open(host_profile,'a') as f:
                f.write(host_str)
        except Exception as e:
            logger.info('{0}文件修改失败！'.format(host_profile))
            logger.info('退出安装！')
            sys.exit(0)
        logger.info('{0}文件修改成功！'.format(host_profile))
        os.system('hostnamectl set-hostname {}'.format(hostname))    
    
    @staticmethod
    def modify_limits_file():
        limit_conf = '''
mysql soft nofile 655360
mysql soft stack 10240
mysql soft nproc 65536\n'''
        limit_conf_file = '/etc/security/limits.conf'
        if os.path.exists(limit_conf_file):
            cp_result = os.system('cp {0} {1}.bak{2}'.format(limit_conf_file,limit_conf_file,
            datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if cp_result == 0:
                logger.info('备份{0}文件成功！'.format(limit_conf_file))
            else:
                logger.info('备份{0}文件失败！'.format(limit_conf_file))
                logger.info('退出安装！')
                sys.exit(0)
        else:
            logger.info('{0}文件不存在，cp备份该文件失败！'.format(limit_conf_file))
            logger.info('退出安装！')
            sys.exit(0)
        try:
            with open(limit_conf_file,'a') as f:
                f.write(limit_conf)
        except Exception as e:
            logger.info('{0}文件修改失败！'.format(limit_conf_file))
            logger.info('退出安装！')
            sys.exit(0)
        logger.info('{0}文件修改成功！'.format(limit_conf_file))
        limit_pam_file = '/etc/pam.d/login'
        limit_pam = '''
#ORACLE SETTING
session required pam_limits.so\n'''
        if os.path.exists(limit_pam_file):
            cp_result = os.system('cp {0} {1}.bak{2}'.format(limit_pam_file,limit_pam_file,
            datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if cp_result == 0:
                logger.info('备份{0}文件成功！'.format(limit_pam_file))
            else:
                logger.info('备份{0}文件失败！'.format(limit_pam_file))
                logger.info('退出安装！')
                sys.exit(0)
        else:
            logger.info('{0}文件不存在，cp备份该文件失败！'.format(limit_pam_file))
            logger.info('退出安装！')
            sys.exit(0)
        try:
            with open(limit_pam_file,'a') as f:
                f.write(limit_pam)
        except Exception as e:
            logger.info('{0}文件修改失败！'.format(limit_pam_file))
            logger.info('退出安装！')
            sys.exit(0)
        logger.info('{0}文件修改成功！'.format(limit_pam_file))

    @staticmethod
    def modify_sysctl_file():
        get_mem_cmd = "free -b | awk '/Mem/ {print $2}'"
        get_page_cmd = "getconf PAGE_SIZE"
        mem = os.popen(get_mem_cmd).read().strip('\n')
        page_size = os.popen(get_page_cmd).read().strip('\n')
        shmmax = int(int(mem) * 0.5)
        shmall = int(int(shmmax) / int(page_size))
        sysctl_config = '''
fs.aio-max-nr = 4194304
fs.file-max = 6815744
kernel.shmmax = {0}
kernel.shmall = {1}
kernel.shmmni = 4096
kernel.sem = 10000 40960000 10000 4096
net.ipv4.ip_local_port_range = 20000 65535
vm.swappiness=1\n'''.format(shmmax,shmall)
        sysctl_file = '/etc/sysctl.conf'
        if os.path.exists(sysctl_file):
            cp_result = os.system('cp {0} {1}.bak{2}'.format(sysctl_file,sysctl_file,
            datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if cp_result == 0:
                logger.info('备份{0}文件成功！'.format(sysctl_file))
            else:
                logger.info('备份{0}文件失败！'.format(sysctl_file))
                logger.info('退出安装！')
                sys.exit(0)
        else:
            logger.info('{0}文件不存在，cp备份该文件失败！'.format(sysctl_file))
            logger.info('退出安装！')
            sys.exit(0)
        try:
            with open(sysctl_file,'a') as f:
                f.write(sysctl_config)
        except Exception as e:
            logger.info('{0}文件修改失败！'.format(sysctl_file))
            logger.info('退出安装！')
            sys.exit(0)
        os.system('sysctl -p > /dev/null 2>&1')
        logger.info('{0}文件修改成功！'.format(sysctl_file))

    @staticmethod
    def create_dir():
        mysql_home_dir = config.get('pre_mysql_install','mysql_home')
        mysql_scripts_dir = mysql_home_dir + '/scripts'
        mysqldata_home_dir = config.get('pre_mysql_install','mysqldata')
        mysqldata_data_dir = mysqldata_home_dir + '/data'
        mysqldata_tmp_dir = mysqldata_home_dir + '/tmp'
        mysqldata_log_dir = mysqldata_home_dir + '/logs'
        mysqlbinlog_home_dir = config.get('pre_mysql_install','mysqlbinlog')
        mysql_relaylog_dir = mysqlbinlog_home_dir + '/relay'
        mysql_backup_dir = config.get('pre_mysql_install','mysqlbackup')
        if not os.path.exists(mysql_home_dir):
            os.makedirs(mysql_home_dir)
            logger.info('目录{0}创建成功！'.format(mysql_home_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysql_home_dir))
        if not os.path.exists(mysql_scripts_dir):
            os.makedirs(mysql_scripts_dir)
            logger.info('目录{0}创建成功！'.format(mysql_scripts_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysql_scripts_dir))
        if not os.path.exists(mysqldata_home_dir):
            os.makedirs(mysqldata_home_dir)
            logger.info('目录{0}创建成功！'.format(mysqldata_home_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysqldata_home_dir))
        if not os.path.exists(mysqldata_data_dir):
            os.makedirs(mysqldata_data_dir)
            logger.info('目录{0}创建成功！'.format(mysqldata_data_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysqldata_data_dir))
        if not os.path.exists(mysqldata_tmp_dir):
            os.makedirs(mysqldata_tmp_dir)
            logger.info('目录{0}创建成功！'.format(mysqldata_tmp_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysqldata_tmp_dir))
        if not os.path.exists(mysqldata_log_dir):
            os.makedirs(mysqldata_log_dir)
            logger.info('目录{0}创建成功！'.format(mysqldata_log_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysqldata_log_dir))
        if not os.path.exists(mysqlbinlog_home_dir):
            os.makedirs(mysqlbinlog_home_dir)
            logger.info('目录{0}创建成功！'.format(mysqlbinlog_home_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysqlbinlog_home_dir))
        if not os.path.exists(mysql_relaylog_dir):
            os.makedirs(mysql_relaylog_dir)
            logger.info('目录{0}创建成功！'.format(mysql_relaylog_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysql_relaylog_dir))
        if not os.path.exists(mysql_backup_dir):
            os.makedirs(mysql_backup_dir)
            logger.info('目录{0}创建成功！'.format(mysql_backup_dir))
        else:
            logger.info('目录{0}已经存在！'.format(mysql_backup_dir))
    
    @staticmethod
    def user_group_add():
        is_group = "egrep '^{0}' /etc/group > /dev/null 2>&1"
        is_user = "egrep '^{0}' /etc/passwd > /dev/null 2>&1"
        mysql_home_dir = config.get('pre_mysql_install','mysql_home')
        mysql_user = config.get('pre_mysql_install','mysql_user')
        mysqluser_cmd = '/usr/sbin/useradd -u 321 -g 320 -M -d {0} {1}'.format(mysql_home_dir,mysql_user)
        mysql_user_pwd = config.get('pre_mysql_install','password')
        mysql_pwd_cmd = '''echo "{0}" | passwd --stdin {1} > /dev/null 2>&1'''.format(mysql_user,mysql_user_pwd)
        mysql_user_group = config.get('pre_mysql_install','mysql_group')
        mysql_group_cmd = '/usr/sbin/groupadd -g 320 {0}'.format(mysql_user_group)
        group_result = os.system(is_group.format(mysql_user_group))
        if group_result != 0:
            os.system(mysql_group_cmd)
            logger.info('mysql用户组创建成功！')
        else:
            logger.info('mysql用户组已经存在！')
        user_result = os.system(is_user.format(mysql_user))
        if user_result != 0:
            os.system(mysqluser_cmd)
            os.system(mysql_pwd_cmd)
            os.system('cp -r /etc/skel/.bashrc /home/db/mysql > /dev/null 2>&1')
            logger.info('mysql用户创建和设置密码成功！')
        else:
            logger.info('mysql用户已经存在！')

    @staticmethod
    def change_dir_priv():
        mysql_home_dir = config.get('pre_mysql_install','mysql_home')
        mysql_scripts_dir = mysql_home_dir + '/scripts'
        mysqldata_home_dir = config.get('pre_mysql_install','mysqldata')
        mysqldata_data_dir = mysqldata_home_dir + '/data'
        mysqldata_tmp_dir = mysqldata_home_dir + '/tmp'
        mysqldata_log_dir = mysqldata_home_dir + '/logs'
        mysqlbinlog_home_dir = config.get('pre_mysql_install','mysqlbinlog')
        mysql_relaylog_dir = mysqlbinlog_home_dir + '/relay'
        mysql_backup_dir = config.get('pre_mysql_install','mysqlbackup')
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysql_home_dir))
        logger.info('目录{0}赋权成功！'.format(mysql_home_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysql_scripts_dir))
        logger.info('目录{0}赋权成功！'.format(mysql_scripts_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysqldata_home_dir))
        logger.info('目录{0}赋权成功！'.format(mysqldata_home_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysqldata_data_dir))
        logger.info('目录{0}赋权成功！'.format(mysqldata_data_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysqldata_tmp_dir))
        logger.info('目录{0}赋权成功！'.format(mysqldata_tmp_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysqldata_log_dir))
        logger.info('目录{0}赋权成功！'.format(mysqldata_log_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysqlbinlog_home_dir))
        logger.info('目录{0}赋权成功！'.format(mysqlbinlog_home_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysql_relaylog_dir))
        logger.info('目录{0}赋权成功！'.format(mysql_relaylog_dir))
        os.system('chown -R mysql:mysql {0} > /dev/null 2>&1'.format(mysql_backup_dir))
        logger.info('目录{0}赋权成功！'.format(mysql_backup_dir))

    @staticmethod
    def modify_bash_profile():
        mysql_home_dir = config.get('pre_mysql_install','mysql_home')
        mysql_profile_config = '''
export MYSQL_HOME={0}
export PATH=$PATH:{1}/bin:{2}/lib
export PS1='$LOGNAME@'`hostname`:'$PWD''$ '
if [ -t 0 ]; then
stty intr ^C
fi\n'''.format(mysql_home_dir,mysql_home_dir,mysql_home_dir)
        mysql_bash_profile = mysql_home_dir + '/.bash_profile'
        try:
            with open(mysql_bash_profile,'w') as f:
                f.write(mysql_profile_config)
            os.system('chown -R mysql:mysql {0}'.format(mysql_bash_profile))
        except Exception as e:
            logger.info('mysql用户的{0}文件修改失败！'.format(mysql_bash_profile))
            logger.info('退出安装！')
            sys.exit(0)
        logger.info('oracle用户的{0}文件修改成功！'.format(mysql_bash_profile))

    @staticmethod
    def modify_profile():
        profile_str = '''export PATH=$PATH:/home/db/mysql/bin:/home/db/mysql/lib\n'''
        profile = '/etc/profile'
        if os.path.exists(profile):
            cp_result = os.system('cp {0} {1}.bak{2}'.format(profile,profile,
            datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if cp_result == 0:
                logger.info('备份{0}文件成功！'.format(profile))
            else:
                logger.info('备份{0}文件失败！'.format(profile))
                logger.info('退出安装！')
                sys.exit(0)
        else:
            logger.info('{0}文件不存在，cp备份该文件失败！'.format(profile))
            logger.info('退出安装！')
            sys.exit(0)
        try:
            with open(profile,'a') as f:
                f.write(profile_str)
            os.system('source {0}'.format(profile))
        except Exception as e:
            logger.info('{0}文件修改失败！'.format(profile))
            logger.info('退出安装！')
            sys.exit(0)
        logger.info('{0}文件修改成功！'.format(profile))

class MysqlInstall(object):
    @staticmethod
    def unzip_mysql_package():
        install_dir = config.get('mysql_install','install_dir') 
        mysql_home_dir = config.get('pre_mysql_install','mysql_home')
        package_name = install_dir + '/' + config.get('mysql_install','package_name')
        mysql_user = config.get('pre_mysql_install','mysql_user')
        if not os.path.exists(package_name):
            logger.info('{}安装包不存在！'.format(package_name))
            logger.info('退出安装！')
            sys.exit(0)
        os.system('chown mysql:mysql {0} > /dev/null 2>&1'.format(package_name))
        result_1 = os.system("su - {0} -c 'tar -zxvf {1} -C {2}' > /dev/null 2>&1".format(mysql_user,package_name,mysql_home_dir))
        if result_1 == 0:
            logger.info('解压mysql压缩包成功！')
        else:
            logger.info('解压mysql压缩包失败！')
            logger.info('退出安装！')
            sys.exit(0)
        src_file = mysql_home_dir + '/' + config.get('mysql_install','package_name').strip('.tar.gz') + '/*'
        dst_dir = mysql_home_dir + '/' 
        result_2 = os.system('mv {0} {1} > /dev/null 2>&1'.format(src_file,dst_dir))
        if result_2 == 0:
            logger.info('移动mysql解压文件到{0}成功！'.format(mysql_home_dir))
        else:
            logger.info('移动mysql解压文件到{0}失败！'.format(mysql_home_dir))
            logger.info('退出安装！')
            sys.exit(0)
        os.system('rm -fr {0} > /dev/null 2>&1'.format(mysql_home_dir + '/' + config.get('mysql_install','package_name').strip('.tar.gz')))
    
    @staticmethod
    def mysql_install():
        server_id = config.get('mysql_install','server_id')
        cpu_count = os.popen('cat /proc/cpuinfo | grep processor | wc -l').read().strip('\n')
        mem_size = os.popen("free -g | grep '^Mem' | awk '{print $2}'").read().strip('\n')
        buffer_pool_size = str(int(int(mem_size) * 0.5)) + 'G'
        mycnf_str = """
[mysql]
port = 13306
socket = /home/db/mysql/mysql.sock
init-command = set names utf8mb4
prompt= \u@\h \\R:\\m:\\s [\d]>
[mysqld]
server-id = {0}   #denpend on server_id rule (slave:20/30/40)
port = 13306
user = mysql
basedir = /home/db/mysql
datadir = /mysqldata/data
tmpdir = /mysqldata/tmp
socket = /home/db/mysql/mysql.sock
character_set_server=utf8mb4
collation_server= utf8mb4_bin
lower_case_table_names=1
pid-file=/mysqldata/data/mysqld.pid
autocommit=0
log_timestamps=SYSTEM
 
############# binlog #############
log-bin=/mysqlbinlog/master-bin #slave-->/mysqlbinlog/slave[n]-bin
binlog_cache_size=2M
expire_logs_days=10
binlog_rows_query_log_events=1
############# replication #############
master_info_repository=table
relay_log_info_repository=table
gtid-mode=ON
enforce-gtid-consistency=ON
log-slave-updates=1
slave_parallel_type=LOGICAL_CLOCK
slave_parallel_workers=4
relay_log=/mysqlbinlog/relay/master-relay-bin #slave--/mysqlbinlog/relay/slave-relay-bin
 
############# slow log #############
slow_query_log=1
slow_query_log_file = /mysqldata/logs/mysql_slow.log
long_query_time = 1
 
############# error log #############
log-error =/mysqldata/logs/mysql_error.log
 
############# thread #############
max_connections = 4000        #dependent on machine
key_buffer_size = 256M
max_allowed_packet = 32M
table_open_cache = 4000
table_open_cache_instances = {1}    #CPU COUNT
sort_buffer_size = 8M
read_rnd_buffer_size=1M
join_buffer_size = 2M
tmp_table_size = 64M
max_heap_table_size = 128M
 
############# innodb #############
innodb_data_file_path=ibdata1:24M:autoextend
innodb_buffer_pool_size = {2}     #physical memory’s 50%
innodb_buffer_pool_instances = {3}    #CPU COUNT
innodb_log_file_size = 1GB
innodb_log_files_in_group = 4
innodb_log_buffer_size = 32M
innodb_lock_wait_timeout = 600
innodb_thread_concurrency = {4}   #CPU COUNT
innodb_flush_method=O_DIRECT
innodb_read_io_threads =16     
innodb_write_io_threads =16   
innodb_io_capacity = 800      
innodb_temp_data_file_path=ibtmp1:12M:autoextend:max:2G
innodb_flush_log_at_timeout=2
log_bin_trust_function_creators=1
transaction_isolation=READ-COMMITTED
innodb_undo_directory=/mysqldata/data
innodb_undo_log_truncate=1
innodb_undo_tablespaces=4
innodb_max_undo_log_size=2G
innodb_purge_rseg_truncate_frequency=16
 
############# safe #############
plugin-load=validate_password.so
validate-password=FORCE_PLUS_PERMANENT
 
############# other #############   
init_file=/home/db/mysql/scripts/performance_collection
default-time-zone='+08:00'\n""".format(server_id,cpu_count,buffer_pool_size,cpu_count,cpu_count)
        mysql_conf_file = '/etc/my.cnf'
        if os.path.exists(mysql_conf_file):
            mv_result = os.system('mv {0} {1}.bak{2}'.format(mysql_conf_file,mysql_conf_file,
            datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if mv_result == 0:
                logger.info('备份{0}文件成功！'.format(mysql_conf_file))
            else:
                logger.info('备份{0}文件失败！'.format(mysql_conf_file))
                logger.info('退出安装！')
                sys.exit(0)
        else:
            logger.info('{0}文件不存在，mv备份该文件失败！'.format(mysql_conf_file))
            logger.info('退出安装！')
            sys.exit(0)
        try:
            with open(mysql_conf_file,'w') as f:
                f.write(mycnf_str)
            os.system('chmod +r {0}'.format(mysql_conf_file))
        except Exception as e:
            logger.info('{0}文件修改失败！'.format(mysql_conf_file))
            logger.info('退出安装！')
            sys.exit(0)
        logger.info('{0}文件修改成功！'.format(mysql_conf_file))
        mysql_home_dir = config.get('pre_mysql_install','mysql_home')
        mysql_user = config.get('pre_mysql_install','mysql_user')
        perform_file = mysql_home_dir + '/scripts/performance_collection'
        perform_str = """
UPDATE performance_schema.setup_consumers SET enabled = 'yes';
UPDATE performance_schema.setup_instruments SET enabled='yes' ,timed='yes';\n"""
        try:
            with open(perform_file,'w') as f:
                f.write(perform_str)
            os.system('chown mysql:mysql {0}'.format(perform_file))
        except Exception as e:
            logger.info('{0}文件修改失败！'.format(perform_file))
            logger.info('退出安装！')
            sys.exit(0)
        logger.info('{0}文件修改成功！'.format(perform_file))
        result = os.system("su - {0} -c '{1}/bin/mysqld --initialize --user={2}' > /dev/null 2>&1".format(mysql_user,mysql_home_dir,mysql_user))
        if result == 0:
            logger.info('mysql初始化成功！')
        else:
            logger.info('mysql初始化失败！')
            logger.info('退出安装！')
            sys.exit(0) 
        result = os.system('cp {0}/support-files/mysql.server /etc/init.d/mysqld'.format(mysql_home_dir))
        if result == 0:
            if result == 0:
                logger.info('拷贝{0}文件成功！'.format('{0}/support-files/mysql.server'.format(mysql_home_dir)))
            else:
                logger.info('拷贝{0}文件失败！'.format('{0}/support-files/mysql.server'.format(mysql_home_dir)))
                logger.info('退出安装！')
                sys.exit(0)
        result = os.system('chmod +x /etc/init.d/mysqld')
        if result == 0:
            if result == 0:
                logger.info('修改/etc/init.d/mysqld文件权限成功！')
            else:
                logger.info('修改/etc/init.d/mysqld文件权限失败！')
                logger.info('退出安装！')
                sys.exit(0)
        mysqld_safe_file = mysql_home_dir + '/bin/mysqld_safe'
        if os.path.exists(mysqld_safe_file):
            cp_result = os.system('cp {0} {1}.bak{2}'.format(mysqld_safe_file,mysqld_safe_file,
            datetime.datetime.today().strftime('%Y%m%d%H%M%S')))
            if cp_result == 0:
                logger.info('备份{0}文件成功！'.format(mysqld_safe_file))
            else:
                logger.info('备份{0}文件失败！'.format(mysqld_safe_file))
                logger.info('退出安装！')
                sys.exit(0) 
        else:
            logger.info('{0}文件不存在，cp备份该文件失败！'.format(mysqld_safe_file))
            logger.info('退出安装！')
            sys.exit(0)
        cmd_1 = '''su - {0} -c "sed -i 's/\/usr\/local\/mysql\/data/\/mysqldata\/data/g' {1}"'''.format(mysql_user,mysqld_safe_file)
        cmd_2 = '''su - {0} -c "sed -i 's/\/usr\/local\/mysql/\/home\/db\/mysql/g' {1}"'''.format(mysql_user,mysqld_safe_file)
        result_1 = os.system(cmd_1)
        result_2 = os.system(cmd_2)
        if result_1 == 0 and result_2 == 0:
            logger.info('{0}文件修改成功！'.format(mysqld_safe_file))
        else:
            logger.info('{0}文件修改失败！'.format(mysqld_safe_file))
            logger.info('退出安装！')
            sys.exit(0)
        os.system('chkconfig mysqld on')
        result = os.system('systemctl enable mysqld')
        if result == 0:
            if result == 0:
                logger.info('添加mysql自启动成功！')
            else:
                logger.info('添加mysql自启动失败！')
                logger.info('退出安装！')
                sys.exit(0)
        result = os.system("su - {0} -c '/etc/init.d/mysqld start' > /dev/null 2>&1".format(mysql_user))
        if result == 0:
            if result == 0:
                logger.info('启动mysql服务成功！')
            else:
                logger.info('启动mysql服务失败！')
                logger.info('退出安装！')
                sys.exit(0)

def main():
    logger.info('=======================硬件配置检查：开始======================')
    HardwareCheck.os_release_check()
    HardwareCheck.os_memory_check()
    HardwareCheck.os_swap_check()
    HardwareCheck.mysql_installdir_check()
    logger.info('=======================硬件配置检查：结束====================\n')
    
    logger.info('==================mysql单机安装前配置：开始==================')
    PreMysqlInstall.stop_firewall()
    PreMysqlInstall.stop_selinux()
    PreMysqlInstall.modify_host()
    PreMysqlInstall.modify_limits_file()
    PreMysqlInstall.modify_sysctl_file()
    PreMysqlInstall.create_dir()
    PreMysqlInstall.user_group_add()
    PreMysqlInstall.change_dir_priv()
    PreMysqlInstall.modify_bash_profile()
    PreMysqlInstall.modify_profile()
    logger.info('==================mysql单机安装前配置：结束==================\n')

    logger.info('==================mysql单机安装：开始==================')
    MysqlInstall.unzip_mysql_package()
    MysqlInstall.mysql_install()
    logger.info('==================mysql单机安装：结束==================\n')

if __name__ == '__main__':
    main()