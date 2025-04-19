# app/schemas/response.py
"""
响应数据结构定义
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SQLGenerationResponse(BaseModel):
    """SQL生成响应"""
    sql: str = Field(..., description="生成的SQL查询")
    confidence: float = Field(..., description="生成的置信度")
    explanation: Optional[str] = Field(None, description="SQL生成的解释")

class QueryResponse(BaseModel):
    """查询响应"""
    success: bool = Field(..., description="查询是否成功")
    question: str = Field(..., description="原始自然语言问题")
    sql: Optional[str] = Field(None, description="生成的SQL查询")
    results: Optional[List[Dict[str, Any]]] = Field(None, description="查询结果")
    columns: Optional[List[str]] = Field(None, description="结果列名")
    error: Optional[str] = Field(None, description="错误信息(如果有)")
    
class TrainingResponse(BaseModel):
    """训练响应"""
    success: bool = Field(..., description="训练是否成功")
    message: str = Field(..., description="训练结果信息")
    training_data_id: Optional[str] = Field(None, description="训练数据ID")