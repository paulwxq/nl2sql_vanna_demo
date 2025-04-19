# app/utils/helpers.py
"""
辅助函数模块
"""
import json
import os
from typing import Dict, Any, List, Optional
import datetime

def load_json_file(file_path: str) -> Any:
    """
    加载JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        Any: 加载的JSON数据
    """
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data: Any, file_path: str) -> bool:
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据
        file_path: 保存路径
        
    Returns:
        bool: 保存是否成功
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

class DateTimeEncoder(json.JSONEncoder):
    """
    自定义JSON编码器，支持序列化日期时间类型
    """
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super().default(obj)

def format_results_for_display(results: List[Dict[str, Any]], columns: List[str]) -> str:
    """
    格式化查询结果用于显示
    
    Args:
        results: 查询结果
        columns: 列名
        
    Returns:
        str: 格式化后的结果字符串
    """
    if not results or not columns:
        return "无结果"
        
    # 计算每列的最大宽度
    widths = {col: len(col) for col in columns}
    for row in results:
        for col in columns:
            if col in row:
                widths[col] = max(widths[col], len(str(row[col])))
    
    # 构建表头
    header = " | ".join(col.ljust(widths[col]) for col in columns)
    separator = "-+-".join("-" * widths[col] for col in columns)
    
    # 构建表格行
    rows = []
    for row in results:
        row_str = " | ".join(
            str(row.get(col, "")).ljust(widths[col]) for col in columns
        )
        rows.append(row_str)
    
    # 组合表格
    table = f"{header}\n{separator}\n" + "\n".join(rows)
    return table 