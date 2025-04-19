# app/config.py
"""
配置文件，包含数据库、LLM、Embedding等配置信息
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'dbname': os.getenv('DB_NAME', 'nl2sql_demo'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
}

# LLM配置
LLM_CONFIG = {
    'provider': 'deepseek',  # 硬编码提供商为deepseek
    'api_uri': os.getenv('LLM_API_URI', ''),
    'api_key': os.getenv('LLM_API_KEY', ''),
    'model': os.getenv('LLM_MODEL', ''),  # 具体的模型名称
    'temperature': float(os.getenv('LLM_TEMPERATURE', '0.1')),
    'max_tokens': int(os.getenv('LLM_MAX_TOKENS', '1024')),
}

# Embedding配置
EMBEDDING_CONFIG = {
    'provider': os.getenv('EMBEDDING_PROVIDER', 'aliyun'),
    'api_uri': os.getenv('EMBEDDING_API_URI', ''),
    'api_key': os.getenv('EMBEDDING_API_KEY', ''),
    'model': os.getenv('EMBEDDING_MODEL', ''),
}

# Vanna配置
VANNA_CONFIG = {
    'collection_name': os.getenv('VANNA_COLLECTION', 'works_dw_vectors'),
    'persist_directory': os.getenv('VANNA_PERSIST_DIR', 'data/vanna_store'),
    'schema': os.getenv('VANNA_SCHEMA', 'nl2vec'),  # 使用nl2vec模式
    'db_impl': os.getenv('VANNA_DB_IMPL', 'pgvector'),  # 使用pgvector
    'api_key': os.getenv('VANNA_API_KEY', 'demo-api-key'),  # Vanna API密钥
    'model_name': os.getenv('VANNA_MODEL_NAME', 'demo-model'),  # Vanna模型名称
    'email': os.getenv('VANNA_EMAIL', 'demo@example.com'),  # Vanna账户邮箱
    'connection_string': None,  # 将在下面动态构建
}

# 日志配置
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.getenv('LOG_FILE', 'logs/nl2sql_demo.log'),
}

# 安全配置
SECURITY_CONFIG = {
    'allowed_operations': ['SELECT'],  # 只允许SELECT操作，防止潜在的危险操作
    'max_query_execution_time': int(os.getenv('MAX_QUERY_TIME', '30')),  # 最大查询执行时间（秒）
}

# 向量存储配置
VECTOR_STORAGE_CONFIG = {
    'schema': 'nl2vec',
    'table_prefix': 'vanna_'
}

# 应用程序存储配置
APP_STORAGE_CONFIG = {
    'schema': 'nl2sql',
    'table_prefix': 'app_'
}