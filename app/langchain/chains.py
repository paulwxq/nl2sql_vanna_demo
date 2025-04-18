# app/langchain/chains.py
"""
自定义LangChain链
"""
import logging
from typing import Dict, Any, List, Optional

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.callbacks.base import CallbackManager

logger = logging.getLogger(__name__)

class SQL2NaturalLanguageChain:
    """
    SQL转自然语言链，用于解释SQL查询
    """
    
    def __init__(self, llm: BaseChatModel):
        """
        初始化SQL解释链
        
        Args:
            llm: LLM模型
        """
        self.llm = llm
        self._create_chain()
    
    def _create_chain(self):
        """创建LangChain链"""
        system_template = """
        你是一位SQL专家，能够将SQL查询转换为清晰的自然语言解释。
        请解释以下SQL查询的含义，使用简单明了的语言，适合非技术人员理解。
        你的解释应该包括：
        1. 这个查询要获取什么数据
        2. 涉及哪些表和字段
        3. 应用了哪些过滤条件或聚合操作
        """
        
        human_template = """
        请解释这个SQL查询：
        ```sql
        {sql}
        ```
        """
        
        system_message = SystemMessagePromptTemplate.from_template(system_template)
        human_message = HumanMessagePromptTemplate.from_template(human_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
        
        self.chain = LLMChain(llm=self.llm, prompt=chat_prompt)
    
    def explain_sql(self, sql: str) -> str:
        """
        解释SQL查询
        
        Args:
            sql: SQL查询语句
            
        Returns:
            str: SQL的自然语言解释
        """
        try:
            result = self.chain.run(sql=sql)
            return result
        except Exception as e:
            logger.error(f"解释SQL错误: {str(e)}")
            return f"无法解释SQL查询: {str(e)}"

class NaturalLanguageRefinementChain:
    """
    自然语言优化链，用于优化用户的查询
    """
    
    def __init__(self, llm: BaseChatModel):
        """
        初始化查询优化链
        
        Args:
            llm: LLM模型
        """
        self.llm = llm
        self._create_chain()
    
    def _create_chain(self):
        """创建LangChain链"""
        system_template = """
        你是一位自然语言查询专家，能够优化用户的数据库查询问题。
        你的任务是将用户可能含糊或不完整的问题转化为明确、具体的数据查询问题。
        请考虑以下方面进行优化：
        1. 明确查询的主题和目标
        2. 指明需要的过滤条件和约束
        3. 确定是否需要排序、分组或聚合
        4. 清晰表达需要返回的数据字段
        """
        
        human_template = """
        用户的原始问题是："{question}"
        
        请将其优化为更明确的数据库查询问题:
        """
        
        system_message = SystemMessagePromptTemplate.from_template(system_template)
        human_message = HumanMessagePromptTemplate.from_template(human_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
        
        self.chain = LLMChain(llm=self.llm, prompt=chat_prompt)
    
    def refine_question(self, question: str) -> str:
        """
        优化用户问题
        
        Args:
            question: 用户原始问题
            
        Returns:
            str: 优化后的问题
        """
        try:
            result = self.chain.run(question=question)
            return result
        except Exception as e:
            logger.error(f"优化问题错误: {str(e)}")
            return question  # 出错时返回原始问题