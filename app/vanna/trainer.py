# app/vanna/trainer.py
"""
Vanna训练模块
"""
import logging
import os
import json
from typing import Dict, Any, List, Optional

from app.utils.helpers import load_json_file, save_json_file
from app.schemas.request import TrainingRequest
from app.schemas.response import TrainingResponse

logger = logging.getLogger(__name__)

class VannaTrainer:
    """
    Vanna训练器，负责训练Vanna模型
    """
    
    def __init__(self, vanna_instance, training_data_dir: str = "data/training"):
        """
        初始化训练器
        
        Args:
            vanna_instance: Vanna实例
            training_data_dir: 训练数据目录
        """
        self.vanna = vanna_instance
        self.training_data_dir = training_data_dir
        
        # 确保训练数据目录存在
        os.makedirs(self.training_data_dir, exist_ok=True)
    
    def train_from_files(self) -> TrainingResponse:
        """
        从训练数据文件中训练Vanna
        
        Returns:
            TrainingResponse: 训练响应
        """
        training_files = [
            os.path.join(self.training_data_dir, "simple_queries.json"),
            os.path.join(self.training_data_dir, "filter_queries.json"),
            os.path.join(self.training_data_dir, "join_queries.json"),
            os.path.join(self.training_data_dir, "complex_queries.json")
        ]
        
        success_count = 0
        error_count = 0
        
        for file_path in training_files:
            if not os.path.exists(file_path):
                logger.warning(f"训练文件不存在: {file_path}")
                continue
                
            try:
                data = load_json_file(file_path)
                if not data:
                    continue
                    
                for item in data:
                    try:
                        request = TrainingRequest(**item)
                        self._train_single_item(request)
                        success_count += 1
                    except Exception as e:
                        logger.error(f"训练单个项目失败: {str(e)}")
                        error_count += 1
                        
            except Exception as e:
                logger.error(f"从文件训练失败: {str(e)}")
                error_count += 1
        
        return TrainingResponse(
            success=(error_count == 0),
            message=f"训练完成: {success_count} 成功, {error_count} 失败",
            training_data_id=None
        )
    
    def train_single_item(self, request: TrainingRequest) -> TrainingResponse:
        """
        训练单个项目
        
        Args:
            request: 训练请求
            
        Returns:
            TrainingResponse: 训练响应
        """
        try:
            training_id = self._train_single_item(request)
            return TrainingResponse(
                success=True,
                message="训练成功",
                training_data_id=training_id
            )
        except Exception as e:
            logger.error(f"训练单个项目失败: {str(e)}")
            return TrainingResponse(
                success=False,
                message=f"训练失败: {str(e)}",
                training_data_id=None
            )
    
    def _train_single_item(self, request: TrainingRequest) -> str:
        """
        训练单个项目的实现
        
        Args:
            request: 训练请求
            
        Returns:
            str: 训练数据ID
        """
        if request.question and request.sql:
            # 训练问题-SQL对
            return self.vanna.add_sql(question=request.question, sql=request.sql)
        elif request.ddl:
            # 训练DDL语句
            return self.vanna.add_ddl(ddl=request.ddl)
        elif request.documentation:
            # 训练文档
            return self.vanna.add_documentation(documentation=request.documentation)
        else:
            raise ValueError("训练请求必须包含问题和SQL、DDL或文档")
    
    def remove_training_data(self, training_data_id: str) -> bool:
        """
        移除训练数据
        
        Args:
            training_data_id: 训练数据ID
            
        Returns:
            bool: 是否成功移除
        """
        try:
            self.vanna.remove_training_data(id=training_data_id)
            return True
        except Exception as e:
            logger.error(f"移除训练数据失败: {str(e)}")
            return False