# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.10.5
@Time    :   2022/8/22 1:34 PM
@Desc    :   通用方法
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from utils.log import Logger
import pymysql
import winreg
import subprocess
import time
import random
import sys
from tidevice import Usbmux
from tidevice import Device
from tidevice._ipautil import IPAReader
import os

logger = Logger(logger='Strke Tool').getlog()


class AndroidFunc:
    def __init__(self):  # 初始化 继承父类QMainWindow
        super(AndroidFunc, self).__init__()  # 设置窗口大小

    @staticmethod
    def get_desktop_size() -> any:
        desktop = QApplication.desktop()
        match desktop.width():
            case 4480:
                index_x = desktop.width() - 1920
            case _:
                index_x = desktop.width()
        index_y = desktop.height()
        return index_x, index_y

    @staticmethod
    def get_day_soup() -> str:
        try:
            today = random.randint(1, 13)
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sql = f"""select daily_soup from daily_soup where day_id='{today}'
                                                       """
            cursor.execute(sql)
            data = cursor.fetchone()
            cursor.close()
            my_db.close()
            return data[0]
        except BaseException as error:
            return '生活独一无二，无需人云亦云'

    @staticmethod
    def sql_con(sql_name):
        match sql_name:
            case 'data_sql':
                my_db = pymysql.connect(
                    host="47.97.10.30",
                    user="webeye_test_info",
                    password="Just8023,./",
                    database="webeye_test_info"
                )
                return my_db
            case _:
                return 'connect error'

    @staticmethod
    def get_id_and_package_name_list():
        try:
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sql = f"""select app_id from android_game_info order by app_id ASC
                                       """
            cursor.execute(sql)
            id_res = cursor.fetchall()
            id_arr = [i[0] for i in id_res]
            sql = f"""select package_name from android_game_info order by app_id ASC
                                       """
            cursor.execute(sql)
            name_res = cursor.fetchall()
            name_arr = [i[0] for i in name_res]
            res_arr = [f"{id_arr[i]}-{name_arr[i]}" for i in range(0, len(id_arr))]
            cursor.close()
            my_db.close()
            return res_arr
        except BaseException as error:
            logger.error(error)
            return ['未成功链接sql,请检查网络情况']

    @staticmethod
    def get_tool_list():
        try:
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sql = f"""select app_id from android_game_info where type='tool' order by app_id ASC
                                       """
            cursor.execute(sql)
            id_res = cursor.fetchall()
            id_arr = [i[0] for i in id_res]
            sql = f"""select package_name from android_game_info where type='tool' order by app_id ASC
                                       """
            cursor.execute(sql)
            name_res = cursor.fetchall()
            name_arr = [i[0] for i in name_res]
            res_arr = [f"{id_arr[i]}-{name_arr[i]}" for i in range(0, len(id_arr))]
            cursor.close()
            my_db.close()
            return res_arr
        except BaseException as error:
            logger.error(error)
            return ['未成功链接sql,请检查网络情况']

    @staticmethod
    def get_game_list():
        try:
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sql = f"""select app_id from android_game_info where type='game' order by app_id ASC
                                       """
            cursor.execute(sql)
            id_res = cursor.fetchall()
            id_arr = [i[0] for i in id_res]
            sql = f"""select package_name from android_game_info where type='game' order by app_id ASC
                                       """
            cursor.execute(sql)
            name_res = cursor.fetchall()
            name_arr = [i[0] for i in name_res]
            res_arr = [f"{id_arr[i]}-{name_arr[i]}" for i in range(0, len(id_arr))]
            cursor.close()
            my_db.close()
            return res_arr
        except BaseException as error:
            logger.error(error)
            return ['未成功链接sql,请检查网络情况']

    @staticmethod
    def get_devices_list():
        result = subprocess.run(['adb', 'devices'], shell=True, capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n')
        devices = []
        for line in output_lines[1:]:
            device_info = line.split('\t')
            if len(device_info) == 2 and device_info[1] == 'device':
                devices.append(device_info[0])
        return devices

    @staticmethod
    def get_specify_data(sql_name, select_key, table_name, select_conditions, conditions_key):
        my_db = AndroidFunc.sql_con(sql_name)
        cursor = my_db.cursor()
        sql = f"""select {select_key} from {table_name} where {select_conditions} = "{conditions_key}"
                                          """
        cursor.execute(sql)
        res = cursor.fetchone()
        return res[0]

    @staticmethod
    def get_desktop():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        my_path = winreg.QueryValueEx(key, "Desktop")[0]
        return my_path

    @staticmethod
    def get_file_path():
        file_path = QFileDialog.getOpenFileName(None, '请选择APP的路径:', AndroidFunc.get_desktop())
        return file_path

    @staticmethod
    def get_existing_directory():
        directory_path = QFileDialog.getExistingDirectory(None, '请选择文件夹的路径', AndroidFunc.get_desktop())
        return directory_path

    @staticmethod
    def subprocess_single(command):
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = res.stdout.readline()
        logger.info(f'执行了cmd命令:{command}')
        return data

    @staticmethod
    def check_file_exist(device_serial, directory, file_name):
        command = f'adb -s {device_serial} shell ls {directory}'
        result = os.popen(command).read().strip()

        # 判断目录下是否存在指定文件
        if file_name in result:
            logger.info(f"目录 {directory} 下存在文件 {file_name}")
            return True
        else:
            logger.error(f"目录 {directory} 下不存在文件 {file_name}")
            return False

    # 多行打印cmd命令
    @staticmethod
    def subprocess_multiple(command):
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = res.stdout.readlines()
        logger.info(f'执行了cmd命令:{command}')
        return data

    # 重写entry内容
    @staticmethod
    def rewrite(entry, keyword):
        entry.setext(keyword)

    @staticmethod
    def subprocess_out(command):
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_data = res.stdout
        return out_data

    @staticmethod
    def subprocess_err(command):
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error_data = res.stderr
        return error_data

    @staticmethod
    def get_current_package_name(devices) -> str:
        try:
            key = f'adb -s {devices} shell dumpsys window | findstr mCurrentFocus'
            res = AndroidFunc.subprocess_out(key).readline().decode('utf-8').strip()
            package_name = res.split(' u0 ')[1].split('/')[0]
            return package_name
        except BaseException as error:
            logger.error(error)

    @staticmethod
    def restart_current_app(devices):
        try:
            package_name = AndroidFunc.get_current_package_name(devices)
            key1 = f"adb -s {devices} shell am force-stop {package_name}"
            AndroidFunc.subprocess_out(key1)
            time.sleep(1)
            key2 = f"adb -s {devices} shell am start -n {package_name}/.UnityMain"
            AndroidFunc.subprocess_out(key2)
        except BaseException as error:
            logger.error(error)

    @staticmethod
    def adb_status():
        res = subprocess.Popen("adb devices", shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = res.stdout.readlines()[1].decode('utf-8').strip()
        if 'device' in data:
            logger.info(f'例行检查adb链接状态：链接正常')
            return True
        else:
            logger.info(f'例行检查adb链接状态：链接已断开')
            return False

    @staticmethod
    def clear_cache(package_name, devices):
        pk_id = ''
        try:
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sql = f"""select app_id from android_game_info where package_name = '{package_name}'
                                        """
            cursor.execute(sql)
            pk_id = cursor.fetchone()
            cursor.close()
            my_db.close()
        except BaseException as error:
            logger.error(error)
        if pk_id:
            key = f"adb -s {devices} shell pm clear {package_name}"
            print(key)
            result = AndroidFunc.subprocess_out(key).readline()
            res = str(result)
            print(res)
            if 'Success' in res:
                return 'success'
            else:
                return 'failed'
        elif 'android' in AndroidFunc.get_current_package_name(devices):
            return 'no running app'
        else:
            current_package = AndroidFunc.get_current_package_name(devices)
            key = f"adb -s {devices} shell pm clear {current_package}"
            AndroidFunc.subprocess_out(key)
            return 'current success'

    @staticmethod
    def get_info(devices):
        try:
            key = f"adb -s {devices} shell getprop ro.product.model"
            name_data = AndroidFunc.subprocess_out(key).readline()
            ad_name = name_data.decode('utf-8')
            key = f"adb -s {devices} shell getprop ro.build.version.release"
            version_data = AndroidFunc.subprocess_out(key).readline()
            ad_version = version_data.decode('utf-8')
            key = f"adb -s {devices} shell wm size"
            size_data = AndroidFunc.subprocess_out(key).readline()
            screen_size = size_data.decode('utf-8')
            return ad_name, ad_version, screen_size
        except BaseException as error:
            logger.error(error)

    @staticmethod
    def restart_adb(devices):
        subprocess.Popen(f"adb -s {devices} kill-server", shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen(f"adb -s {devices} devices", shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    """
    IOS Func
    """

    # 获取 udid
    @staticmethod
    def get_ios_udid():
        try:
            udid = str(Usbmux().device_list()).split("', device_id=")[0].split("='")[1]
            return udid
        except BaseException as error:
            return '您当前的未链接设备，请链接设备'

    @staticmethod
    def install(res):
        try:
            ipa_path = AndroidFunc.get_file_path()
            if 'ipa' in ipa_path[0]:
                Device(res).app_install(ipa_path[0])
                return True
            else:
                return '您选择的文件不是ipa格式，请重新选择'
        except BaseException as error:
            return error

    @staticmethod
    def uninstall(res, bundle_id):
        try:
            Device(res).app_uninstall(bundle_id)
            return True
        except BaseException as error:
            return error

    @staticmethod
    def restart_ipa(res, bundle_id):
        try:
            pid = Device(res).app_start(bundle_id, kill_running=True)
            return pid
        except BaseException as error:
            return error

    @staticmethod
    def show_ios_info():
        try:
            key = 'tidevice info'
            result = AndroidFunc.subprocess_multiple(key)
            return result
        except BaseException as error:
            return error

    @staticmethod
    def screenshot(res, flag):
        desktop_path = AndroidFunc.get_desktop()
        file_path = fr"{desktop_path}\screenshot{flag}.jpg"
        try:
            Device(res).screenshot().convert("RGB").save(file_path)
            return f'截图成功,图片保存在：{file_path}'
        except BaseException as error:
            return str(error)

    @staticmethod
    def get_bundle_id() -> str:
        ipa_path = AndroidFunc.get_file_path()
        ir = IPAReader(ipa_path[0])
        bundle_id = ir.get_bundle_id()
        return bundle_id

    @staticmethod
    def get_code_and_des():
        code = [3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017,
                3018, 3019, 3020, 3021, 3101, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 3112, 3113,
                3114, 3115, 3116, 3117, 3118, 3119, 3120, 3121, 3122, 3123, 3124, 3125, 3126, 3127, 3128, 3129, 3130,
                3131, 3132, 3133, 3201, 3202, 3203, 3204, 3205, 3206, 3207, 3208, 3209, 3210, 3211, 3212, 3213, 3214,
                3215, 3299, 3301, 3302, 3303, 3304, 3305, 3306, 3307, 3308, 3309, 3310, 3311, 3312, 3313, 3314, 3315,
                3316, 3317, 3318, 3319, 3320, 3321, 3322, 3323, 3324, 3325, 3326, 3327, 3328, 3329, 3330, 3331, 3332,
                3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3343, 3344, 3345, 3346, 3347, 3348, 3349,
                3350, 3351, 3352, 3353, 3354, 3355, 3356, 3401, 3402, 3403, 3404, 3405, 3406, 3407, 3515, 4001, 4002,
                4003, 4004, 4005, 4006, 4007, 4008, 4009, 4010, 4011, 4012, 4013, 4014, 4015]
        des = ['失败', '请求参数错误', '签名错误', '服务器错误-接口异常', '请求消息格式无效-一般为json格式不正确',
               '用户设备id不匹配-请求的id与注册时不一致', '内部服务请求[X-SECRET-KEY]错误',
               '内部服务请求未携带[X-SECRET-KEY]', 'Rox-Token无效', 'Rox-Token过期', '请求未授权', '请升级到最新版本',
               'request is invalid-请求时间戳超期', 'trace_level[1]级别需要提供trace id', '服务器请求消息头错误',
               '服务器请求未携带指定消息头', 'app id is invalid-应用id在广告平台未配置',
               '未知微信应用-产品未配置微信参数', '获取微信授权token失败', '获取微信用户信息失败', '用户IP在黑名单中',
               '用户不存在', '用户设备已注销', '用户设备与did不一致', '不支持的绑定社交账号类型',
               '获取facebook服务器信息失败', 'fb账号已经被其他用户绑定', '当前用户已经绑定了其他fb账号',
               '获取google服务器信息失败', 'google账号已经被其他用户绑定', '当前用户已经绑定了其他google账号',
               '获取apple服务器信息失败', 'apple账号已经被其他用户绑定', '当前用户已经绑定了其他apple账号',
               '用户未绑定微信', '用户微信信息异常', '此微信已绑定过其他账号', '此用户已经绑定过其他微信账号',
               '后台配置错误, 请检查', '支付宝服务异常', '支付宝请求异常', '支付宝响应异常',
               '此支付宝账号已绑定其他用户', '此用户已经绑定其他支付宝账号', '徒弟未绑定社交账号', '师傅未绑定社交账号',
               '当前用户没有师傅', '当前用户的师傅不存在', '获取支付宝access_token失败', '获取支付宝用户信息失败',
               '用户未绑定支付宝', '钱包类型不支持绑定', '钱包信息已经被其他用户绑定',
               '当前用户已经绑定了同类型的其他钱包信息', '宗门未启用', '当前师傅的宗门信息不存在',
               '获取宗门配置信息失败', '宗门邀请人数不达标', '宗门奖励已经领取', '宗门邀请的人数不是有效的值',
               '宗门异变步骤无效', '宗门异变步骤未配置', '宗门异变贡献值不够', '当前用户的宗门未创建',
               '当前用户已经被其他宗门师傅邀请', '不能邀请自己加入自己的宗门', '绑定宗门师傅关系超时',
               '你的师傅宗门未创建', '你已经有宗门徒弟', '宗门接口内部错误', '异常用户, 无法提现',
               '用户身份信息异常,已用于其他设备提现', '今天提现次数已达上限', '提现任务的提现次数达到上限',
               '当前提现任务的全局次数达到上限', '极速提现预算超期', '请求的提现通道无效',
               '当前提现任务的每天可用次数已超限', '提现任务的类型不正确', '提现任务id已存在', '提现任务id不存在',
               '不支持当前的提现方法', '用户账号已注销', '提现通道的商户号异常', '提现通道异常', '用户应用版本太低',
               '无效的手机号码', '无效的提现任务的付款类型', '提现任务的付款类型错误', '拒绝极速提现',
               '三方提现接口操作失败', '话费产品code不存在', '话费产品的面值和请求金额不一致', '提现请求流水号已存在',
               '不支持当前国家的话费提现', '提现订单查询接口参数不正确', '提现订单不存在', '极速提现请求的金额超限',
               '用户实名信息为空', '手机号可充值次数达到上限', '黑名单用户, 请联系客服',
               '申请人年龄条件不符, 请使用其他身份信息提现', '无效的姓名, 请检查',
               '注销过的用户再次注册并提现，此类用户禁止提现', '提现失败', '产品未配置兑付，需联系财务配置',
               '兑付方式配置错误，需联系财务', '产品未配置兑付，需联系财务配置', '单用户每天可调用3次实名认证',
               '用户实名认证异常', '提现任务和提现类型不一致', '提现金额非法, 请检查', '不是有效的钱包类型',
               '海外现金提现操作失败', '小于目前微信支持的最小金额0.3元', '当前国家的兑付功能已关闭',
               '第三方服务器兑付接口功能已关闭', '当前用户未绑定电子钱包，不能提现到钱包', '产品可能已下架',
               '产品支持的面值发生变化', '礼品卡库存不足', '接口操作失败', '礼品卡未激活',
               '收款账号达到可以被使用的最大用户数', '用户注册时间和安装时间的间隔过大',
               '用户提现不满足内部PayPal提现要求', '应用微信提现权限未开通', '单笔提现金额超过微信商户限制',
               '该用户微信实名信息不正确', '用户微信支付账户未实名, 无法付款', '用户今日付款次数超过限制',
               '已达到今日商户付款额度上限', '用户已达到今日收款额度上限', '提现被Aegis 拦截',
               '未提供待修改的APP系统配置数据', 'APP系统配置KEY不存在', 'APP宗门裂变配置已创建',
               '未创建当前APP宗门裂变配置', 'APP系统配置值无效', '每日极速提现付款预算配置过小, 请检查',
               'APP国家系统配置不存在, 请检查', '仅存在当前唯一APP国家系统配置, 不能删除',
               '超出极速提现金额上限, 请检查', '查询条件开始时间必须小于结束时间, 请检查', '请选择要操作的提现记录',
               '提现订单操作失败', '不存在可用的兑付供应商', '兑付供应商不支持当前国家', '话费供应商应用ID未配置']
        dictionary = dict(zip(code, des))
        return code, dictionary


if __name__ == '__main__':
    pass
