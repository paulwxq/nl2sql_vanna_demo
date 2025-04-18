# app/__init__.py
"""
NL2SQL Demo 应用包
"""
import logging
from app.utils.logger import setup_logging

# 初始化日志
setup_logging()
logger = logging.getLogger(__name__)
logger.info("初始化NL2SQL Demo应用")