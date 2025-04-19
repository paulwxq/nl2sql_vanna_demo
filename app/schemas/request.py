# app/schemas/request.py
"""
请求数据结构定义
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class NLQueryRequest(BaseModel):
    """自然语言查询请求"""
    question: str = Field(..., description="自然语言问题")
    context: Optional[Dict[str, Any]] = Field(None, description="查询上下文信息")
    max_results: Optional[int] = Field(100, description="最大返回结果数")

class FeedbackRequest(BaseModel):
    """用户反馈请求"""
    question: str = Field(..., description="原始自然语言问题")
    sql: str = Field(..., description="生成的SQL查询")
    is_correct: bool = Field(..., description="SQL是否正确")
    correct_sql: Optional[str] = Field(None, description="用户提供的正确SQL(如果有)")
    
class TrainingRequest(BaseModel):
    """训练数据请求"""
    question: Optional[str] = Field(None, description="自然语言问题")
    sql: Optional[str] = Field(None, description="SQL查询")
    ddl: Optional[str] = Field(None, description="数据定义语言语句")
    documentation: Optional[str] = Field(None, description="文档说明")