# app/db/connection.py
"""
数据库连接管理模块
"""
import logging
import time
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Optional, Tuple, List, Dict, Any

from app.config import DATABASE_CONFIG, SECURITY_CONFIG
from app.db.security import SQLSecurityFilter

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """数据库连接管理类，提供连接池和执行查询的功能"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化数据库连接
        
        Args:
            config: 数据库配置，如果为None则使用默认配置
        """
        self.config = config or DATABASE_CONFIG
        self._engine = None
        self.connect()
    
    def connect(self):
        """创建数据库连接引擎"""
        connection_string = (
            f"postgresql+psycopg2://{self.config['user']}:{self.config['password']}@"
            f"{self.config['host']}:{self.config['port']}/{self.config['dbname']}"
        )
        try:
            self._engine = create_engine(
                connection_string,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800,
            )
            
            # 简单测试连接是否成功
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                
            logger.info(f"成功连接到数据库 {self.config['dbname']} at {self.config['host']}:{self.config['port']}")
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            logger.error("请确保数据库已经存在并且表结构已经创建")
            raise
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接上下文管理器"""
        if not self._engine:
            self.connect()
        
        connection = self._engine.connect()
        try:
            yield connection
        finally:
            connection.close()
    
    def execute_query(self, sql: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        执行SQL查询并返回结果
        
        Args:
            sql: SQL查询语句
            
        Returns:
            Tuple[List[Dict], List[str]]: 查询结果和列名列表
        """
        # 检查SQL是否安全
        security_filter = SQLSecurityFilter(SECURITY_CONFIG)
        safe_sql = security_filter.validate_and_sanitize(sql)
        
        rows = []
        column_names = []
        
        try:
            with self.get_connection() as conn:
                # 设置查询超时
                conn.execute(text(f"SET statement_timeout = {SECURITY_CONFIG['max_query_execution_time'] * 1000}"))
                
                # 执行查询
                start_time = time.time()
                result = conn.execute(text(safe_sql))
                end_time = time.time()
                
                # 处理结果
                column_names = result.keys()
                for row in result:
                    rows.append({column: value for column, value in zip(column_names, row)})
                
                logger.info(f"查询执行成功，用时 {end_time - start_time:.3f} 秒，返回 {len(rows)} 条结果")
                
        except SQLAlchemyError as e:
            logger.error(f"查询执行错误: {str(e)}")
            raise
            
        return rows, list(column_names)
    
    def get_database_schema(self) -> str:
        """
        获取数据库结构DDL
        
        Returns:
            str: 数据库DDL语句
        """
        schema_ddl = []
        
        try:
            inspector = inspect(self._engine)
            
            # 获取所有表
            for schema in inspector.get_schema_names():
                if schema in ('pg_catalog', 'information_schema'):
                    continue
                    
                for table_name in inspector.get_table_names(schema=schema):
                    # 构建CREATE TABLE语句
                    columns = []
                    primary_keys = inspector.get_pk_constraint(table_name, schema=schema)['constrained_columns']
                    
                    for column in inspector.get_columns(table_name, schema=schema):
                        col_def = f"{column['name']} {column['type']}"
                        
                        if not column.get('nullable', True):
                            col_def += " NOT NULL"
                            
                        if column['name'] in primary_keys:
                            col_def += " PRIMARY KEY"
                            
                        columns.append(col_def)
                    
                    # 外键关系
                    foreign_keys = []
                    for fk in inspector.get_foreign_keys(table_name, schema=schema):
                        fk_def = (
                            f"FOREIGN KEY ({', '.join(fk['constrained_columns'])}) "
                            f"REFERENCES {fk['referred_schema']}.{fk['referred_table']}({', '.join(fk['referred_columns'])})"
                        )
                        foreign_keys.append(fk_def)
                    
                    # 构建完整的CREATE TABLE语句
                    create_table = f"CREATE TABLE {schema}.{table_name} (\n"
                    create_table += ",\n".join(columns)
                    
                    if foreign_keys:
                        create_table += ",\n" + ",\n".join(foreign_keys)
                        
                    create_table += "\n);"
                    schema_ddl.append(create_table)
            
            return "\n\n".join(schema_ddl)
            
        except Exception as e:
            logger.error(f"获取数据库结构失败: {str(e)}")
            raise

    def get_connection_info(self) -> Dict[str, Any]:
        """
        获取数据库连接信息
        
        Returns:
            Dict[str, Any]: 数据库连接信息
        """
        return {
            'host': self.config['host'],
            'port': self.config['port'],
            'dbname': self.config['dbname'],
            'user': self.config['user'],
            'password': self.config['password']
        }