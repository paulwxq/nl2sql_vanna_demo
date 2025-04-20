"""
从数据库提取schema并存储到Vanna
"""
import os
import sys
import argparse
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.logger import setup_logging
from app.db.connection import DatabaseConnection
from app.vanna.setup import VannaSetup
from app.langchain.llm_config import LLMFactory, EmbeddingFactory

def extract_and_save_schema(force=False):
    """
    从数据库提取schema并存储到Vanna
    
    Args:
        force: 是否强制更新已有schema
    """
    # 初始化日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # 初始化数据库连接
        logger.info("连接数据库...")
        db_connection = DatabaseConnection()
        
        # 初始化Vanna，直接传入数据库连接
        logger.info("初始化Vanna...")
        llm_model = LLMFactory.create_llm()
        embedding_model = EmbeddingFactory.create_embedding()
        vanna_setup = VannaSetup(llm_model, embedding_model)
        vanna_instance = vanna_setup.initialize_vanna(db_connection=db_connection)
        
        # 手动提取schema
        logger.info("从数据库提取schema...")
        db_schema = db_connection.get_database_schema()
        
        # 如果强制更新，先尝试清除旧的schema数据
        if force:
            logger.info("强制更新模式：尝试清除现有schema...")
            try:
                # 使用数据库连接直接执行SQL
                with db_connection._engine.connect() as conn:
                    conn.execute("TRUNCATE TABLE IF EXISTS nl2vec.vanna_schemas")
                    conn.commit()
                logger.info("成功清除现有schema数据")
            except Exception as e:
                logger.warning(f"清除现有schema数据失败，将继续添加新schema: {str(e)}")
        
        # 添加schema到Vanna
        logger.info("向Vanna添加数据库schema...")
        training_id = vanna_instance.add_ddl(db_schema)
        
        logger.info(f"成功提取并存储数据库schema，训练ID: {training_id}")
        return True
    except Exception as e:
        logger.error(f"提取和存储schema失败: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='从数据库提取schema并存储到Vanna')
    parser.add_argument('--force', action='store_true', help='强制更新已有schema')
    args = parser.parse_args()
    
    success = extract_and_save_schema(args.force)
    
    if success:
        print("成功提取并存储数据库schema")
    else:
        print("提取和存储schema失败，请查看日志了解详情")
        sys.exit(1)

if __name__ == "__main__":
    main() 