# app/vanna/setup.py
"""
Vanna初始化模块，负责设置和配置Vanna
"""
import logging
import os
from typing import Dict, Any, Optional, List, Tuple
import re

# 更新导入语句，使用langchain-community而不是langchain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAI
from vanna.pgvector import PGVector

# 导入数据库连接库
import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import VANNA_CONFIG, LLM_CONFIG, EMBEDDING_CONFIG

logger = logging.getLogger(__name__)

class VannaSetup:
    """
    Vanna设置类，负责初始化和配置Vanna
    """
    
    def __init__(self, llm_model: Optional[ChatOpenAI] = None, 
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
    
    def initialize_vanna(self, db_connection=None):
        """
        初始化Vanna实例，使用混合模式
        
        Args:
            db_connection: 可选，数据库连接实例。如果提供，将直接配置数据库连接
        
        Returns:
            对象: 初始化后的Vanna实例
        
        Raises:
            Exception: 当初始化失败时抛出异常
        """
        # 导入Vanna
        import vanna
        
        # 1. 创建自定义LLM实现（不再继承LLM基类）
        class LangChainLLM:
            def __init__(self, llm_model):
                self.llm_model = llm_model
            
            def ask(self, prompt: str, **kwargs):
                """调用LangChain LLM模型"""
                try:
                    response = self.llm_model.invoke(prompt)
                    return response.content
                except Exception as e:
                    logger.error(f"LLM请求失败: {str(e)}")
                    raise e
        
        # 2. 创建自定义Embedding实现（不再继承Embed基类）
        class LangChainEmbed:
            def __init__(self, embedding_model):
                self.embedding_model = embedding_model
            
            def embed(self, text: str) -> List[float]:
                """生成文本的向量嵌入"""
                try:
                    return self.embedding_model.embed_query(text)
                except Exception as e:
                    logger.error(f"嵌入生成失败: {str(e)}")
                    raise e
            
            def embed_documents(self, documents: List[str]) -> List[List[float]]:
                """生成多个文档的向量嵌入"""
                try:
                    return self.embedding_model.embed_documents(documents)
                except Exception as e:
                    logger.error(f"批量嵌入生成失败: {str(e)}")
                    raise e
        
        # 准备数据库连接信息和向量存储
        vector_store = None
        if db_connection:
            db_info = db_connection.get_connection_info()
            
            # 创建PGVector向量存储
            collection_name = self.config.get('collection_name', 'vanna_vectors')
            schema_name = self.config.get('schema', 'nl2vec')
            
            # 使用单独参数而非connection_string
            vector_store = PGVector(
                host=db_info['host'],
                port=db_info['port'],
                user=db_info['user'],
                password=db_info['password'],
                database=db_info['dbname'],  # 注意这里的参数名是database而不是dbname
                collection_name=collection_name,
                schema_name=schema_name,
                embedding_function=self.embedding_model
            )
            logger.info(f"已配置PGVector向量存储: {schema_name}.{collection_name}@{db_info['dbname']}")
        
        # 3. 初始化Vanna
        # 使用PGVector向量存储
        vanna_instance = vanna.Vanna(
            config={
                'collection_name': self.config.get('collection_name', 'vanna_collection'),
                'persist_directory': self.config.get('persist_directory', 'data/vanna_store'),
                'db_impl': self.config.get('db_impl', 'pgvector'),
                'schema': self.config.get('schema', 'nl2vec')
            },
            llm=LangChainLLM(self.llm_model),
            embedding=LangChainEmbed(self.embedding_model),
            vector_store=vector_store
        )
        
        logger.info(f"使用本地Vanna + 混合模式 (自定义LLM + PGVector) 初始化成功")
        self.vanna_instance = vanna_instance
        
        return self.vanna_instance
