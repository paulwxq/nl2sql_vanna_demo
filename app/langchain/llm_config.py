# app/langchain/llm_config.py
"""
LLM模型配置模块，用于初始化和配置LLM模型
"""
import logging
from typing import Dict, Any, Optional, List

#from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI

from app.config import LLM_CONFIG, EMBEDDING_CONFIG

logger = logging.getLogger(__name__)

class LLMFactory:
    """
    LLM工厂类，用于创建不同的LLM模型实例
    """
    
    @staticmethod
    def create_llm(config: Dict[str, Any] = None) -> ChatOpenAI:
        """
        创建LLM模型实例
        
        Args:
            config: LLM配置
            
        Returns:
            ChatOpenAI: LangChain LLM模型实例
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
    def _create_deepseek_llm(config: Dict[str, Any]) -> ChatOpenAI:
        """
        创建DeepSeek LLM实例
        
        Args:
            config: LLM配置
            
        Returns:
            ChatOpenAI: DeepSeek LLM实例
        """
        # 获取配置参数
        model_name = config.get('model', 'deepseek-chat')
        api_base = config.get('api_uri', '')
        api_key = config.get('api_key', '')
        temperature = config.get('temperature', 0.1)
        max_tokens = config.get('max_tokens', 1024)
        
        # 创建自定义DeepSeek适配器
        return ChatOpenAI(
            model_name=model_name,
            openai_api_base=api_base,
            openai_api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    @staticmethod
    def _create_qwen_llm(config: Dict[str, Any]) -> ChatOpenAI:
        """
        创建Qwen LLM实例
        
        Args:
            config: LLM配置
            
        Returns:
            ChatOpenAI: Qwen LLM实例
        """
        # 获取配置参数
        model_name = config.get('model', 'qwen')
        api_base = config.get('api_uri', '')
        api_key = config.get('api_key', '')
        temperature = config.get('temperature', 0.1)
        max_tokens = config.get('max_tokens', 1024)
        
        # 创建自定义Qwen适配器
        return ChatOpenAI(
            model_name=model_name,
            openai_api_base=api_base,
            openai_api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )

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
        from langchain_core.embeddings import Embeddings
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