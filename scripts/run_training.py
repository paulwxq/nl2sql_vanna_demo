"""
执行Vanna训练的简单脚本
要先执行generate_training_data.py，生成四个json数据集，然后再执行当前的脚本，加载那四个json数据集
"""
import os
import sys
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.logger import setup_logging
from app.db.connection import DatabaseConnection
from app.vanna.setup import VannaSetup
from app.vanna.trainer import VannaTrainer
from app.langchain.llm_config import LLMFactory, EmbeddingFactory

def main():
    # 初始化日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("初始化Vanna...")
    # 初始化数据库连接
    db_connection = DatabaseConnection()
    
    # 初始化Vanna
    llm_model = LLMFactory.create_llm()
    embedding_model = EmbeddingFactory.create_embedding()
    vanna_setup = VannaSetup(llm_model, embedding_model)
    vanna = vanna_setup.initialize_vanna(db_connection)
    
    # 创建训练器
    logger.info("开始训练...")
    trainer = VannaTrainer(vanna)
    
    # 调用train_from_files方法
    result = trainer.train_from_files()
    
    logger.info(f"训练结果: {result.message}")

if __name__ == "__main__":
    main() 