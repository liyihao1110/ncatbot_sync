import os
import sys
import logging
import colorama
from logging.handlers import TimedRotatingFileHandler

colorama.init()

# 日志目录配置
LOG_DIR = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志格式配置（固定levelname宽度）
LOG_FORMAT = '[%(asctime)s]%(name)-7s %(levelname)-8s ➜ %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# ANSI 转义序列配置
COLOR_CONFIG = {
    'TIME': '\033[90;3m',        # 浅灰色 + 斜体（分号分隔多个样式）
    'NAME': '\033[1;34m',        # 粗体浅蓝色（1=粗体，34=蓝色）
    'DEBUG': '\033[3;36m',       # 斜体青色（3=斜体在前）
    'INFO': '\033[32m',          # 普通绿色
    'WARNING': '\033[33m',       # 普通黄色
    'ERROR': '\033[31;1m',       # 粗体红色
    'CRITICAL': '\033[1;4;31m',  # 粗体+下划线红色（4=下划线）
    'RESET': '\033[0m'           # 重置所有样式
}


class ColorFormatter(logging.Formatter):
    """支持多字段颜色定制的格式化器"""
    def format(self, record):
        # 生成原始消息组成部分
        asctime = self.formatTime(record, self.datefmt)
        levelname = record.levelname.ljust(8)# 确保levelname宽度为8
        name = record.name.ljust(7)
        message = record.getMessage()
        
        # 构建彩色消息
        colored_asctime = f"{COLOR_CONFIG['TIME']}{asctime}{COLOR_CONFIG['RESET']}"
        colored_name = f"{COLOR_CONFIG['NAME']}{name}{COLOR_CONFIG['RESET']}"
        colored_level = f"{COLOR_CONFIG[record.levelname]}{levelname}{COLOR_CONFIG['RESET']}"
        
        # 处理异常信息
        if record.exc_info:
            message += "\n" + self.formatException(record.exc_info)
        
        return f"{colored_asctime} {colored_name} {colored_level} ➜ {message}"

def init_logger(name='ncbot', level=logging.DEBUG):
    """初始化并返回配置好的logger对象"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    # 控制台Handler（彩色输出）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColorFormatter())

    # 文件Handler（无颜色格式）
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, 'ncbot.log'),
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

def get_logger(name="main", level=logging.INFO):
    """获取logger实例"""
    return init_logger(name, level)
