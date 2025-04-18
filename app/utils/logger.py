# app/utils/logger.py
"""
日志工具模块
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from app.config import LOGGING_CONFIG

def setup_logging():
    """
    设置日志配置
    """
    # 确保日志目录存在
    log_dir = os.path.dirname(LOGGING_CONFIG['file'])
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # 配置文件处理器
    file_handler = RotatingFileHandler(
        LOGGING_CONFIG['file'],
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(LOGGING_CONFIG['format']))
    root_logger.addHandler(file_handler)
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOGGING_CONFIG['format']))
    root_logger.addHandler(console_handler)
    
    # 设置其他模块的日志级别
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)