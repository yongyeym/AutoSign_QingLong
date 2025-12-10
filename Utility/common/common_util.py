import os
import logging
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Union, Optional

from Utility import notify

def get_os_env(*args: str) -> tuple:
    """
    获取对应的环境变量值，并去除前后空格，可一次获取多个环境变量
    :arg *args：环境变量的Key，可以是多个
    :return 返回的值可以使用一个变量接收为数组列表（只获取一个变量时也需使用下标[0]来获取返回值），也可以分别赋予多个变量单独接收，如果不存在此环境变量，则返回None。
    """
    return tuple(
        value.strip() if value is not None else None
        for value in (os.getenv(arg) for arg in args)
    )

def get_timestamp(input_time: Optional[Union[datetime, str]] = None, type: str = "ms") -> int:
    """
    获取当前时间戳
    :param type:时间戳精度，默认为毫秒级13位数字，反之为秒级10位数字
    :param input_time:需要转时间戳的时间，默认为当前系统时间
    :return 返回时间戳
    """
    if input_time is None:
        input_time = datetime.now()
    elif not isinstance(input_time, datetime):
        try:
            #  使用ISO标准格式化字符串为datetime
            input_time = datetime.fromisoformat(input_time)
        except ValueError:
            try:
                #  使用自定义的格式，格式化字符串为datetime
                input_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                raise ValueError(f"无法转化为时间戳，传入的字符串无法解析为时间日期: {input_time}") from e
    return int(input_time.timestamp()*1000 if type == "ms" else input_time.timestamp())

def get_format_timestamp(timestamp: int, format: str = "%Y年%m月%d日 %H:%M:%S") -> str:
    """
    将时间戳格式化为时间日期的可视化文本
    :param timestamp:时间戳
    :param format:格式化的格式，默认为 年月日 时分秒
    :return 返回格式化后的时间日期文本
    """
    return datetime.fromtimestamp(int(timestamp)).strftime(format)

def get_format_datetime(input_time: Optional[Union[datetime, str]] = None) -> Dict[str, str]:
    """
    获取格式化后的时间日期
    :param input_time:需要格式化的时间日期原数据，默认为当前系统时间
    :return 返回包含所有时间格式的字典
    """
    if input_time is None:
        input_time = datetime.now()
    elif not isinstance(input_time, datetime):
        try:
            #  使用ISO标准格式化字符串为datetime
            input_time = datetime.fromisoformat(input_time)
        except ValueError:
            try:
                #  使用自定义的格式，格式化字符串为datetime
                input_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                raise ValueError(f"无法转化为时间戳，传入的字符串无法解析为时间日期: {input_time}") from e
    date = input_time.strftime("%Y年%m月%d日")  #处理为 年月日 格式
    time = input_time.strftime("%H:%M:%S")  #处理为 时分秒 格式
    datetime_all = input_time.strftime("%Y年%m月%d日 %H:%M:%S")  #处理为 年月日 时分秒 格式
    now_weekday = f"{['星期一','星期二','星期三','星期四','星期五','星期六','星期日'][input_time.weekday()]}"  #处理为 星期 格式
    now_year = f"{input_time.year}"  # 处理为 当前年份 格式
    now_month = "{:02d}".format(input_time.month)  #处理为 当前月份 格式，且不足2位时前面补0
    now_day = "{:02d}".format(input_time.day)  # 处理为 当前日期 格式，且不足2位时前面补0
    return {"date": date, "time": time, "datetime": datetime_all, "weekday": now_weekday, "complete_time": datetime_all + " " + now_weekday, "year": now_year, "month": now_month, "day": now_day}  #返回包含所有格式的字典

def get_uuid(uuid_type: int = 4, need_upper: bool = True, need_hex: bool = False) -> str:
    """
    获取一个通用唯一标识符UUID，英文字母大写
    get_uuid返回的是一般格式的UUID，如 8BC5D95B-F573-52F5-065B-34F37C700956
    get_uuid_hex返回的是去掉UUID的-之后的UUID，如 8BC5D95BF57352F5065B34F37C700956

    uuid版本：
    UUID1基于时间戳、MAC地址、随机数
    UUID3基于命名空间和名称的MD5
    UUID4基于随机数
    UUID5基于命名空间和名称的SHA-1

    uuid命名空间：
    NAMESPACE_DNS基于DNS地址
    NAMESPACE_URL基于URL网址
    NAMESPACE_OID基于ISO OID
    NAMESPACE_X500基于X.500 DN

    :param uuid_type：使用哪一种UUID算法 1/3/4/5，传入参数错误或未传入时使用UUID4
    :param need_upper：是否需要大写输出，默认为是
    :param need_hex：是否需要转为32位十六进制字符串，即去掉UUID中的间隔符横杠-，默认为否
    :return 返回生成的随机UUID字符串，默认为UUID4生成的标准格式大写字符串
    """
    if uuid_type == 1:
        new_uuid = uuid.uuid1()
    elif uuid_type == 3:
        new_uuid = uuid.uuid3(uuid.NAMESPACE_URL, "example.com")  # 暂不考虑使用此方法，此处仅写出使用方式
    elif uuid_type == 4:
        new_uuid = uuid.uuid4()
    elif uuid_type == 5:
        new_uuid = uuid.uuid5(uuid.NAMESPACE_URL, "example.com")  # 暂不考虑使用此方法，此处仅写出使用方式
    else:
        new_uuid = uuid.uuid4()
    if need_hex:
        new_uuid = new_uuid.hex
    new_uuid = str(new_uuid)  # 进行字符串化
    if need_upper:
        new_uuid.upper()
    return new_uuid

def get_md5(content: str) -> str:
    """
    :param content:需要计算MD5的文本
    :return:返回文本的MD5
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def send_notify(title: str, content: str = "无详细信息，请查看日志！"):
    """
    发送通知推送，使用青龙自带的notify服务，需要在青龙配置中提前配置好任意推送渠道的key
    :param title：标题
    :param content：详细内容
    """
    now_time = get_format_datetime()["datetime"]
    text = f"结束时间：\n\n{now_time}\n\n运行详情：\n\n{content}"
    notify.send(title, text)

def send_log(log_level: int, content: str):
    """
    发送Log日志。basicConfig 日志基本配置：level 最低显示的日志级别
    :param log_level：日志级别：0 信息 | 1 警告 | 2 错误 | 3 致命错误 | 其他 DEBUG
    :param content：详细日志内容
    """
    logging.basicConfig(
        level=logging.INFO,  # 设置日志级别
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y年%m月%d日 %H:%M:%S',
        encoding = "utf-8"
    )
    if log_level == 0:
        logging.info(content)
    elif log_level == 1:
        logging.warning(content)
    elif log_level == 2:
        logging.error(content)
    elif log_level == 3:
        logging.critical(content)
    else:
        logging.debug(content)

class SPException(Exception):
    """
    主动抛出异常，用于中断后续无效的函数执行并直接进行最后的通知推送
    使用 raise SPException("title", "content") 主动抛出
    """
    def __init__(self, title: str = "意外的错误", content: str = "请查看日志！"):
        self.title = title
        self.content = content
        super().__init__(self.title)
    def __str__(self):
        e2str = f"【{self.title}】\n\n错误详情为：" + self.content  # 定义直接输出e时的显示文本
        return e2str