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
        """
        try:
            # 导入Vanna
            import vanna
            from vanna.pgvector import PostgreSQL
            
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
                        return None
            
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
                        return []
                
                def embed_documents(self, documents: List[str]) -> List[List[float]]:
                    """生成多个文档的向量嵌入"""
                    try:
                        return self.embedding_model.embed_documents(documents)
                    except Exception as e:
                        logger.error(f"批量嵌入生成失败: {str(e)}")
                        return [[] for _ in documents]
            
            # 准备数据库连接信息
            postgres_config = {}
            if db_connection:
                db_info = db_connection.get_connection_info()
                postgres_config = {
                    'host': db_info['host'],
                    'port': db_info['port'],
                    'dbname': db_info['dbname'],
                    'user': db_info['user'],
                    'password': db_info['password']
                }
                logger.info(f"已配置PostgreSQL数据库连接: {db_info['dbname']}@{db_info['host']}")
            
            # 3. 初始化Vanna
            # 使用本地PostgreSQL向量存储
            vanna_instance = vanna.Vanna(
                config={
                    'collection_name': self.config.get('collection_name', 'vanna_collection'),
                    'persist_directory': self.config.get('persist_directory', 'data/vanna_store'),
                    'db_impl': self.config.get('db_impl', 'pgvector'),
                    'schema': self.config.get('schema', 'nl2vec')
                },
                llm=LangChainLLM(self.llm_model),
                embedding=LangChainEmbed(self.embedding_model),
                # 使用pgvector存储向量，并传入数据库连接信息
                vector_store=PostgreSQL(**postgres_config)
            )
            
            logger.info(f"使用本地Vanna + 混合模式 (自定义LLM + pgvector) 初始化成功")
            self.vanna_instance = vanna_instance
            
        except Exception as e:
            logger.error(f"本地Vanna初始化失败: {str(e)}")
            # 如果本地模式失败，使用模拟模式
            self.vanna_instance = self.create_mock_vanna()
            logger.info("使用模拟Vanna实例")
        
        return self.vanna_instance    
    def create_mock_vanna(self):
        """
        创建模拟Vanna对象，用于演示
        
        Returns:
            对象: 模拟的Vanna实例
        """
        class MockVanna:
            def generate_sql(self, question):
                # 返回一个简单的SQL查询
                return f"SELECT * FROM users LIMIT 10; -- 查询: {question}"
                
            def add_sql(self, question, sql):
                # 模拟添加SQL
                return "mock-training-id"
                
            def add_ddl(self, ddl):
                # 模拟添加DDL
                return "mock-ddl-id"
                
            def add_documentation(self, documentation):
                # 模拟添加文档
                return "mock-doc-id"
                
            def remove_training_data(self, id):
                # 模拟删除训练数据
                return True
            
            def train(self, question=None, sql=None, ddl=None, documentation=None):
                # 兼容Vanna 0.7.x API
                if question and sql:
                    return self.add_sql(question, sql)
                elif ddl:
                    return self.add_ddl(ddl)
                elif documentation:
                    return self.add_documentation(documentation)
                return None
        
        return MockVanna()
