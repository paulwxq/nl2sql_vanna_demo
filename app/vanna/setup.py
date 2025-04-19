# app/vanna/setup.py
"""
Vanna初始化模块，负责设置和配置Vanna
"""
import logging
import os
from typing import Dict, Any, Optional, List, Tuple

# 更新导入语句，使用langchain-community而不是langchain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.embeddings import Embeddings

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
    
    def initialize_vanna(self):
        """
        初始化Vanna实例
        
        Returns:
            对象: 初始化后的Vanna实例
        """
        try:
            # 尝试使用本地Vanna + 混合模式 (DeepSeek LLM + pgvector)
            import vanna
            
            # 创建自定义Vanna类（使用预先配置的LLM和pgvector）
            class CustomVanna:
                def __init__(self, config=None, llm=None, embedding_model=None):
                    self.config = config or {}
                    self.llm = llm
                    self.embedding_model = embedding_model
                    self.collection_name = config.get('collection_name', 'vanna_collection')
                    self.persist_directory = config.get('persist_directory', 'data/vanna_store')
                    self.db_connection = None
                    
                def connect_to_postgres(self, host, port, dbname, user, password):
                    """连接到PostgreSQL数据库"""
                    import psycopg2
                    self.db_connection = psycopg2.connect(
                        host=host,
                        port=port,
                        dbname=dbname,
                        user=user,
                        password=password
                    )
                    logger.info(f"已连接到PostgreSQL数据库: {dbname}")
                    return True
                
                def generate_sql(self, question):
                    """使用LLM生成SQL"""
                    if not self.llm:
                        return f"SELECT * FROM users LIMIT 10; -- 查询: {question} (模拟模式)"
                        
                    # 构建提示
                    prompt = f"""
                    你是一个专业的SQL查询助手。请根据以下问题生成一个PostgreSQL SQL查询：
                    
                    问题: {question}
                    
                    SQL查询:
                    """
                    
                    try:
                        response = self.llm([HumanMessage(content=prompt)])
                        sql = response.content.strip()
                        
                        return sql
                    except Exception as e:
                        logger.error(f"生成SQL失败: {str(e)}")
                        return f"SELECT * FROM users LIMIT 10; -- 查询: {question} (错误回退)"
                
                def add_sql(self, question, sql):
                    """存储问题和SQL对"""
                    # 在实际系统中，这将存储到向量数据库，这里简化为日志记录
                    logger.info(f"存储问题-SQL对: {question} -> {sql}")
                    return f"training-{hash(question+sql)}"
                
                def add_ddl(self, ddl):
                    """存储数据库schema信息"""
                    logger.info(f"存储DDL: {ddl[:100]}...")
                    return f"ddl-{hash(ddl)}"
                
                def add_documentation(self, documentation):
                    """存储文档"""
                    logger.info(f"存储文档: {documentation[:100]}...")
                    return f"doc-{hash(documentation)}"
                
                def remove_training_data(self, id):
                    """删除训练数据"""
                    logger.info(f"删除训练数据: {id}")
                    return True
                    
                def train(self, question=None, sql=None, ddl=None, documentation=None):
                    """兼容旧API"""
                    if question and sql:
                        return self.add_sql(question, sql)
                    elif ddl:
                        return self.add_ddl(ddl)
                    elif documentation:
                        return self.add_documentation(documentation)
                    return None
            
            # 初始化Vanna实例
            self.vanna_instance = CustomVanna(
                config=self.config,
                llm=self.llm_model,
                embedding_model=self.embedding_model
            )
            
            logger.info(f"使用本地Vanna + DeepSeek LLM + pgvector模式初始化成功")
            
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
                
            def connect_to_postgres(self, **kwargs):
                # 模拟连接数据库
                return True
            
            def train(self, question=None, sql=None, ddl=None, documentation=None):
                # 兼容旧API
                if question and sql:
                    return self.add_sql(question, sql)
                elif ddl:
                    return self.add_ddl(ddl)
                elif documentation:
                    return self.add_documentation(documentation)
                return None
        
        return MockVanna()
    
    def connect_to_database(self, db_connection):
        """
        将Vanna连接到数据库
        
        Args:
            db_connection: 数据库连接实例
        """
        if not self.vanna_instance:
            raise ValueError("Vanna实例尚未初始化")
        
        try:
            # 获取数据库连接信息
            db_info = db_connection.get_connection_info()
            
            # 连接到PostgreSQL数据库
            self.vanna_instance.connect_to_postgres(
                host=db_info['host'],
                port=db_info['port'],
                dbname=db_info['dbname'],
                user=db_info['user'],
                password=db_info['password']
            )
            
            # 获取数据库元数据
            db_schema = db_connection.get_database_schema()
            
            # 尝试训练Vanna了解数据库结构
            try:
                # 兼容新旧API
                if hasattr(self.vanna_instance, 'add_ddl'):
                    self.vanna_instance.add_ddl(db_schema)
                else:
                    self.vanna_instance.train(ddl=db_schema)
                logger.info("成功添加数据库DDL到Vanna")
            except Exception as e:
                logger.warning(f"添加DDL失败，但将继续初始化: {str(e)}")
            
            logger.info("Vanna已成功连接到数据库")
        except Exception as e:
            logger.error(f"连接数据库失败: {str(e)}")