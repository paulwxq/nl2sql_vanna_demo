# app/vanna/query_processor.py
"""
查询处理模块，用于处理自然语言查询并生成SQL
"""
import logging
from typing import Dict, Any, List, Optional, Tuple

from app.db.connection import DatabaseConnection

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    查询处理器，负责处理自然语言查询，生成SQL并执行
    """
    
    def __init__(self, vanna_instance, db_connection: DatabaseConnection):
        """
        初始化查询处理器
        
        Args:
            vanna_instance: Vanna实例
            db_connection: 数据库连接实例
        """
        self.vanna = vanna_instance
        self.db_connection = db_connection
    
    def process_query(self, question: str) -> Dict[str, Any]:
        """
        处理自然语言查询
        
        Args:
            question: 自然语言问题
            
        Returns:
            Dict: 包含SQL查询、结果和元数据的字典
        """
        logger.info(f"处理查询: {question}")
        
        try:
            # 使用Vanna生成SQL
            sql = self.vanna.generate_sql(question=question)
            
            if not sql:
                logger.warning(f"未能为问题生成SQL: {question}")
                return {
                    "success": False,
                    "error": "无法根据您的问题生成SQL查询，请尝试重新表述您的问题。",
                    "question": question,
                    "sql": None,
                    "results": None,
                    "columns": None
                }
            
            logger.info(f"生成的SQL: {sql}")
            
            # 执行SQL查询
            results, columns = self.db_connection.execute_query(sql)
            
            return {
                "success": True,
                "question": question,
                "sql": sql,
                "results": results,
                "columns": columns
            }
            
        except Exception as e:
            logger.error(f"查询处理错误: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "question": question,
                "sql": None,
                "results": None,
                "columns": None
            }
    
    def train_from_feedback(self, question: str, sql: str, is_correct: bool = True) -> bool:
        """
        根据用户反馈训练Vanna
        
        Args:
            question: 自然语言问题
            sql: SQL查询
            is_correct: 指示SQL是否正确
            
        Returns:
            bool: 训练是否成功
        """
        if not is_correct:
            logger.info(f"用户反馈SQL不正确，跳过训练: {sql}")
            return False
            
        try:
            # 训练问题-SQL对
            self.vanna.add_sql(question=question, sql=sql)
            logger.info(f"成功训练问题-SQL对: {question} -> {sql}")
            return True
        except Exception as e:
            logger.error(f"训练错误: {str(e)}")
            return False