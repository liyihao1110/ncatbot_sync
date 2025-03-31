import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
# 日志目录配置
LOG_DIR = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志格式配置
LOG_FORMAT = '%(asctime)s %(name)s %(levelname)s %(filename)s[line:%(lineno)d] ➜ %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

# ANSI 转义序列，用于彩色日志
LOG_COLORS = {
    'DEBUG': '\033[36m',    # 青色
    'INFO': '\033[32m',     # 绿色
    'WARNING': '\033[33m',  # 黄色
    'ERROR': '\033[31m',    # 红色
    'CRITICAL': '\033[1;31m'  # 粗体红色
}
RESET_COLOR = '\033[0m'

class ColorFormatter(logging.Formatter):
    """自定义日志格式化器，支持彩色输出"""
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, '')
        message = super().format(record)
        return f"{log_color}{message}{RESET_COLOR}"

def init_logger(name='APP', level=logging.DEBUG):
    """初始化并返回配置好的logger对象"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 控制台Handler（输出到终端，彩色日志）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColorFormatter(LOG_FORMAT, DATE_FORMAT))

    # 文件Handler（按天轮转，保留7天，普通日志）
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, 'app.log'),
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

# 初始化默认logger
def get_logger(name='main', level=logging.INFO):
    """获取logger实例"""
    return init_logger(name, level)
