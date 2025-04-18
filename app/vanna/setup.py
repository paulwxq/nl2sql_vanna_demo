# app/vanna/setup.py
"""
Vanna初始化模块，负责设置和配置Vanna
"""
import logging
import os
from typing import Dict, Any, Optional, List, Tuple

from langchain.chat_models.base import BaseChatModel
from langchain.embeddings.base import Embeddings

from app.config import VANNA_CONFIG, LLM_CONFIG, EMBEDDING_CONFIG

logger = logging.getLogger(__name__)

class VannaSetup:
    """
    Vanna设置类，负责初始化和配置Vanna
    """
    
    def __init__(self, llm_model: Optional[BaseChatModel] = None, 
                embedding_model: Optional[Embeddings] = None,
                vanna_config: Dict[str, Any] = None):
        """
        初始化Vanna设置
        
        Args:
            llm_model: LangChain LLM模型
            embedding_model: LangChain Embedding模型
            vanna_config: Vanna配置
        """
        self.config = vanna_config or VANNA_CONFIG
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.vanna_instance = None
        
        # 确保持久化目录存在
        os.makedirs(self.config['persist_directory'], exist_ok=True)
    
    def initialize_vanna(self):
        """
        初始化Vanna实例
        
        Returns:
            对象: 初始化后的Vanna实例
        """
        from vanna import LangChain_Chat
        from vanna import ChromaDB_VectorStore
        
        # 创建自定义Vanna类
        class CustomVanna(ChromaDB_VectorStore, LangChain_Chat):
            def __init__(self, config=None):
                ChromaDB_VectorStore.__init__(self, config=config)
                LangChain_Chat.__init__(self, config=config)
        
        # 构建Vanna配置
        vanna_config = {
            'collection_name': self.config['collection_name'],
            'persist_directory': self.config['persist_directory'],
            'llm': self.llm_model,
            'embedding_model': self.embedding_model
        }
        
        # 初始化Vanna
        self.vanna_instance = CustomVanna(config=vanna_config)
        logger.info(f"Vanna实例初始化成功，使用集合: {self.config['collection_name']}")
        
        return self.vanna_instance
    
    def connect_to_database(self, db_connection):
        """
        将Vanna连接到数据库
        
        Args:
            db_connection: 数据库连接实例
        """
        if not self.vanna_instance:
            raise ValueError("Vanna实例尚未初始化")
        
        # 获取数据库元数据
        db_schema = db_connection.get_database_schema()
        
        # 训练Vanna了解数据库结构
        self.vanna_instance.train(ddl=db_schema)
        logger.info("Vanna已成功连接到数据库并训练了数据库结构")