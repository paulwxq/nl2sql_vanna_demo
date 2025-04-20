# scripts/generate_training_data.py
"""
生成训练数据脚本
"""
import os
import sys
import json
import argparse
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.logger import setup_logging
from app.utils.helpers import save_json_file

def generate_simple_queries():
    """
    生成简单查询示例
    
    Returns:
        List[Dict]: 简单查询示例列表
    """
    return [
        {
            "question": "列出所有客户",
            "sql": "SELECT * FROM Customers"
        },
        {
            "question": "显示客户总数",
            "sql": "SELECT COUNT(*) FROM Customers"
        },
        {
            "question": "获取所有产品及其价格",
            "sql": "SELECT ProductName, Price FROM Products"
        },
        {
            "question": "列出所有员工的姓名和职位",
            "sql": "SELECT FirstName, LastName, Title FROM Employees"
        },
        {
            "question": "显示所有部门",
            "sql": "SELECT * FROM Departments"
        }
    ]

def generate_filter_queries():
    """
    生成条件过滤查询示例
    
    Returns:
        List[Dict]: 条件过滤查询示例列表
    """
    return [
        {
            "question": "查找名为John的客户",
            "sql": "SELECT * FROM Customers WHERE FirstName = 'John'"
        },
        {
            "question": "找出价格超过100的产品",
            "sql": "SELECT * FROM Products WHERE Price > 100"
        },
        {
            "question": "查找2023年之后入职的员工",
            "sql": "SELECT * FROM Employees WHERE HireDate >= '2023-01-01'"
        },
        {
            "question": "查找纽约的客户",
            "sql": "SELECT * FROM Customers WHERE City = 'New York'"
        },
        {
            "question": "找出库存少于20的产品",
            "sql": "SELECT * FROM Products WHERE StockQuantity < 20"
        }
    ]

def generate_join_queries():
    """
    生成连接查询示例
    
    Returns:
        List[Dict]: 连接查询示例列表
    """
    return [
        {
            "question": "显示每个订单的客户名称",
            "sql": "SELECT o.OrderID, c.FirstName, c.LastName FROM Orders o JOIN Customers c ON o.CustomerID = c.CustomerID"
        },
        {
            "question": "列出每个员工所属的部门",
            "sql": "SELECT e.FirstName, e.LastName, d.DepartmentName FROM Employees e JOIN Departments d ON e.DepartmentID = d.DepartmentID"
        },
        {
            "question": "显示订单中的产品详情",
            "sql": "SELECT o.OrderID, p.ProductName, oi.Quantity, p.Price FROM Orders o JOIN OrderItems oi ON o.OrderID = oi.OrderID JOIN Products p ON oi.ProductID = p.ProductID"
        },
        {
            "question": "查找每个部门的员工数量",
            "sql": "SELECT d.DepartmentName, COUNT(e.EmployeeID) as EmployeeCount FROM Departments d LEFT JOIN Employees e ON d.DepartmentID = e.DepartmentID GROUP BY d.DepartmentName"
        },
        {
            "question": "显示每个客户的订单总数",
            "sql": "SELECT c.FirstName, c.LastName, COUNT(o.OrderID) as OrderCount FROM Customers c LEFT JOIN Orders o ON c.CustomerID = o.CustomerID GROUP BY c.CustomerID, c.FirstName, c.LastName"
        }
    ]

def generate_complex_queries():
    """
    生成复杂查询示例
    
    Returns:
        List[Dict]: 复杂查询示例列表
    """
    return [
        {
            "question": "查找购买金额最高的前5名客户",
            "sql": """
                SELECT c.FirstName, c.LastName, SUM(oi.Quantity * p.Price) as TotalAmount
                FROM Customers c
                JOIN Orders o ON c.CustomerID = o.CustomerID
                JOIN OrderItems oi ON o.OrderID = oi.OrderID
                JOIN Products p ON oi.ProductID = p.ProductID
                GROUP BY c.CustomerID, c.FirstName, c.LastName
                ORDER BY TotalAmount DESC
                LIMIT 5
            """
        },
        {
            "question": "找出每个产品的平均订购数量",
            "sql": """
                SELECT p.ProductName, AVG(oi.Quantity) as AvgQuantity
                FROM Products p
                JOIN OrderItems oi ON p.ProductID = oi.ProductID
                GROUP BY p.ProductID, p.ProductName
            """
        },
        {
            "question": "查找从未被订购过的产品",
            "sql": """
                SELECT p.*
                FROM Products p
                LEFT JOIN OrderItems oi ON p.ProductID = oi.ProductID
                WHERE oi.OrderItemID IS NULL
            """
        },
        {
            "question": "计算每个部门的平均工资",
            "sql": """
                SELECT d.DepartmentName, AVG(e.Salary) as AvgSalary
                FROM Departments d
                JOIN Employees e ON d.DepartmentID = e.DepartmentID
                GROUP BY d.DepartmentID, d.DepartmentName
            """
        },
        {
            "question": "找出每个月的销售总额",
            "sql": """
                SELECT 
                    EXTRACT(YEAR FROM o.OrderDate) as Year,
                    EXTRACT(MONTH FROM o.OrderDate) as Month,
                    SUM(oi.Quantity * p.Price) as TotalSales
                FROM Orders o
                JOIN OrderItems oi ON o.OrderID = oi.OrderID
                JOIN Products p ON oi.ProductID = p.ProductID
                GROUP BY EXTRACT(YEAR FROM o.OrderDate), EXTRACT(MONTH FROM o.OrderDate)
                ORDER BY Year, Month
            """
        }
    ]

def generate_and_save_training_data(output_dir="data/training"):
    """
    生成并保存训练数据
    
    Args:
        output_dir: 输出目录
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成各类查询
    simple_queries = generate_simple_queries()
    filter_queries = generate_filter_queries()
    join_queries = generate_join_queries()
    complex_queries = generate_complex_queries()
    
    # 保存到文件
    save_json_file(simple_queries, os.path.join(output_dir, "simple_queries.json"))
    save_json_file(filter_queries, os.path.join(output_dir, "filter_queries.json"))
    save_json_file(join_queries, os.path.join(output_dir, "join_queries.json"))
    save_json_file(complex_queries, os.path.join(output_dir, "complex_queries.json"))
    
    logger.info(f"训练数据已生成并保存到 {output_dir}")
    logger.info(f"简单查询: {len(simple_queries)} 条")
    logger.info(f"过滤查询: {len(filter_queries)} 条")
    logger.info(f"连接查询: {len(join_queries)} 条")
    logger.info(f"复杂查询: {len(complex_queries)} 条")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='生成Vanna训练数据')
    parser.add_argument('--output-dir', default='data/training', help='训练数据输出目录')
    args = parser.parse_args()
    
    generate_and_save_training_data(args.output_dir)