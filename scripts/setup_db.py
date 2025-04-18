# scripts/setup_db.py
"""
数据库设置脚本
"""
import os
import sys
import argparse
import logging
from sqlalchemy import create_engine, text

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import DATABASE_CONFIG
from app.utils.logger import setup_logging

def setup_database(force=False):
    """
    设置数据库
    
    Args:
        force: 是否强制重建数据库
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # 创建没有指定数据库名称的连接字符串
    connection_string = (
        f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
        f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/postgres"
    )
    
    try:
        # 连接到默认数据库
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # 检查数据库是否存在
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_CONFIG['dbname']}'")
            ).fetchone()
            
            if result and not force:
                logger.info(f"数据库 {DATABASE_CONFIG['dbname']} 已存在，跳过创建")
            else:
                # 如果数据库存在并且强制重建，先删除它
                if result and force:
                    logger.info(f"强制重建数据库 {DATABASE_CONFIG['dbname']}")
                    # 断开所有连接
                    conn.execute(text(
                        f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
                        f"FROM pg_stat_activity "
                        f"WHERE pg_stat_activity.datname = '{DATABASE_CONFIG['dbname']}' "
                        f"AND pid <> pg_backend_pid()"
                    ))
                    conn.execute(text(f"DROP DATABASE IF EXISTS {DATABASE_CONFIG['dbname']}"))
                
                # 创建数据库
                conn.execute(text(f"CREATE DATABASE {DATABASE_CONFIG['dbname']}"))
                logger.info(f"创建数据库 {DATABASE_CONFIG['dbname']} 成功")
        
        # 连接到新创建的数据库
        db_connection_string = (
            f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
            f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"
        )
        db_engine = create_engine(db_connection_string)
        
        # 读取并执行schema文件
        schema_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'schema')
        
        # 读取表定义文件
        tables_file = os.path.join(schema_dir, 'tables.sql')
        if os.path.exists(tables_file):
            with open(tables_file, 'r', encoding='utf-8') as f:
                tables_sql = f.read()
                
            with db_engine.connect() as conn:
                conn.execute(text(tables_sql))
                conn.commit()
            logger.info("创建表成功")
        
        # 读取关系定义文件
        relationships_file = os.path.join(schema_dir, 'relationships.sql')
        if os.path.exists(relationships_file):
            with open(relationships_file, 'r', encoding='utf-8') as f:
                relationships_sql = f.read()
                
            with db_engine.connect() as conn:
                conn.execute(text(relationships_sql))
                conn.commit()
            logger.info("创建关系成功")
        
        # 读取并执行种子数据文件
        seed_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed', 'seed_data.sql')
        if os.path.exists(seed_file):
            with open(seed_file, 'r', encoding='utf-8') as f:
                seed_sql = f.read()
                
            with db_engine.connect() as conn:
                conn.execute(text(seed_sql))
                conn.commit()
            logger.info("插入种子数据成功")
            
        logger.info("数据库设置完成")
        
    except Exception as e:
        logger.error(f"设置数据库时出错: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='设置数据库')
    parser.add_argument('--force', action='store_true', help='强制重建数据库')
    args = parser.parse_args()
    
    setup_database(args.force)