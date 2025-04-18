# app/langchain/llm_config.py
"""
LLM模型配置模块，用于初始化和配置LLM模型
"""
import logging
from typing import Dict, Any, Optional, List

from langchain.chat_models.base import BaseChatModel
from langchain.schema import SystemMessage
from langchain.embeddings.base import Embeddings

from app.config import LLM_CONFIG, EMBEDDING_CONFIG

logger = logging.getLogger(__name__)

class LLMFactory:
    """
    LLM工厂类，用于创建不同的LLM模型实例
    """
    
    @staticmethod
    def create_llm(config: Dict[str, Any] = None) -> BaseChatModel:
        """
        创建LLM模型实例
        
        Args:
            config: LLM配置
            
        Returns:
            BaseChatModel: LangChain LLM模型实例
        """
        config = config or LLM_CONFIG
        provider = config.get('provider', 'deepseek').lower()
        
        if provider == 'deepseek':
            return LLMFactory._create_deepseek_llm(config)
        elif provider == 'qwen':
            return LLMFactory._create_qwen_llm(config)
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}")
    
    @staticmethod
    def _create_deepseek_llm(config: Dict[str, Any]) -> BaseChatModel:
        """
        创建DeepSeek LLM实例
        
        Args:
            config: LLM配置
            
        Returns:
            BaseChatModel: DeepSeek LLM实例
        """
        from langchain.chat_models import ChatOpenAI
        
        # 创建自定义DeepSeek适配器
        class DeepSeekAdapter(ChatOpenAI):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.model_name = config.get('model', 'deepseek-chat')
                self.openai_api_base = config.get('api_uri')
                self.openai_api_key = config.get('api_key')
                self.temperature = config.get('temperature', 0.1)
                self.max_tokens = config.get('max_tokens', 1024)
                
                # 设置系统提示
                self.system_message = SystemMessage(content=(
                    "你是一个专业的SQL查询助手，能够根据自然语言生成准确的SQL查询。"
                    "请确保生成的SQL查询是安全的，并且只包含SELECT操作。"
                ))
        
        return DeepSeekAdapter()
    
    @staticmethod
    def _create_qwen_llm(config: Dict[str, Any]) -> BaseChatModel:
        """
        创建Qwen LLM实例
        
        Args:
            config: LLM配置
            
        Returns:
            BaseChatModel: Qwen LLM实例
        """
        from langchain.chat_models import ChatOpenAI
        
        # 创建自定义Qwen适配器
        class QwenAdapter(ChatOpenAI):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.model_name = config.get('model', 'qwen')
                self.openai_api_base = config.get('api_uri')
                self.openai_api_key = config.get('api_key')
                self.temperature = config.get('temperature', 0.1)
                self.max_tokens = config.get('max_tokens', 1024)
                
                # 设置系统提示
                self.system_message = SystemMessage(content=(
                    "你是一个专业的SQL查询助手，能够根据自然语言生成准确的SQL查询。"
                    "请确保生成的SQL查询是安全的，并且只包含SELECT操作。"
                ))
        
        return QwenAdapter()

class EmbeddingFactory:
    """
    Embedding工厂类，用于创建Embedding模型实例
    """
    
    @staticmethod
    def create_embedding(config: Dict[str, Any] = None) -> Embeddings:
        """
        创建Embedding模型实例
        
        Args:
            config: Embedding配置
            
        Returns:
            Embeddings: LangChain Embedding模型实例
        """
        config = config or EMBEDDING_CONFIG
        provider = config.get('provider', 'aliyun').lower()
        
        if provider == 'aliyun':
            return EmbeddingFactory._create_aliyun_embedding(config)
        else:
            raise ValueError(f"不支持的Embedding提供商: {provider}")
    
    @staticmethod
    def _create_aliyun_embedding(config: Dict[str, Any]) -> Embeddings:
        """
        创建阿里云Embedding实例
        
        Args:
            config: Embedding配置
            
        Returns:
            Embeddings: 阿里云Embedding实例
        """
        from langchain.embeddings.base import Embeddings
        import requests
        
        # 创建自定义阿里云Embedding适配器
        class AliyunEmbedding(Embeddings):
            def __init__(self, api_uri: str, api_key: str, model: str):
                self.api_uri = api_uri
                self.api_key = api_key
                self.model = model
                
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                """Embed多个文档"""
                embeddings = []
                
                for text in texts:
                    embedding = self.embed_query(text)
                    embeddings.append(embedding)
                    
                return embeddings
                
            def embed_query(self, text: str) -> List[float]:
                """Embed单个查询"""
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                payload = {
                    "model": self.model,
                    "input": text
                }
                
                response = requests.post(
                    self.api_uri,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    raise ValueError(f"Embedding API返回错误: {response.text}")
                    
                data = response.json()
                embedding = data.get("data", [{}])[0].get("embedding", [])
                
                return embedding
        
        return AliyunEmbedding(
            api_uri=config.get('api_uri', ''),
            api_key=config.get('api_key', ''),
            model=config.get('model', '')
        )