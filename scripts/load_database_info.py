# scripts/load_database_info.py
"""
向Vanna添加数据库信息的脚本
包含多种方法：直接添加DDL、添加表注释文档、从数据库自动提取注释
"""
import os
import sys
import argparse
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.logger import setup_logging
from app.db.connection import DatabaseConnection
from app.vanna.setup import VannaSetup
from app.langchain.llm_config import LLMFactory, EmbeddingFactory


def add_ddl_from_file(vanna_instance, file_path):
    """从文件添加DDL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ddl_content = f.read()
        
        training_id = vanna_instance.add_ddl(ddl=ddl_content)
        logging.info(f"DDL从文件 {file_path} 添加成功，训练ID: {training_id}")
        return True
    except Exception as e:
        logging.error(f"从文件添加DDL失败: {str(e)}")
        return False

def add_documentation_from_file(vanna_instance, file_path):
    """从文件添加表文档"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
        
        training_id = vanna_instance.add_documentation(documentation=doc_content)
        logging.info(f"表文档从文件 {file_path} 添加成功，训练ID: {training_id}")
        return True
    except Exception as e:
        logging.error(f"从文件添加表文档失败: {str(e)}")
        return False

def extract_and_add_comments(vanna_instance, db_connection):
    """从数据库提取并添加注释"""
    try:
        # 查询表和列的注释
        comments_query = """
        SELECT 
            t.table_name,
            tc.column_name,
            pgd.description as table_comment,
            pgcd.description as column_comment
        FROM 
            pg_catalog.pg_statio_all_tables as st
            INNER JOIN pg_catalog.pg_description pgd ON pgd.objoid = st.relid
            LEFT JOIN information_schema.tables t ON t.table_schema = st.schemaname AND t.table_name = st.relname
            LEFT JOIN information_schema.columns tc ON tc.table_schema = st.schemaname AND tc.table_name = st.relname
            LEFT JOIN pg_catalog.pg_description pgcd ON pgcd.objoid = st.relid AND pgcd.objsubid = tc.ordinal_position
        WHERE
            t.table_schema = 'public'
        ORDER BY 
            t.table_name, tc.ordinal_position;
        """
        
        results, _ = db_connection.execute_query(comments_query)
        
        if not results:
            logging.warning("未找到表或列注释")
            return False
            
        # 格式化注释为文档
        documentation = "# 数据库表和列的注释\n\n"
        current_table = None
        
        for row in results:
            table_name = row.get('table_name')
            column_name = row.get('column_name')
            table_comment = row.get('table_comment')
            column_comment = row.get('column_comment')
            
            if current_table != table_name:
                current_table = table_name
                documentation += f"## {table_name}\n"
                if table_comment:
                    documentation += f"{table_comment}\n\n"
                documentation += "### 字段说明\n"
            
            if column_name and column_comment:
                documentation += f"- {column_name}: {column_comment}\n"
        
        # 添加到Vanna
        training_id = vanna_instance.add_documentation(documentation=documentation)
        logging.info(f"数据库注释提取并添加成功，训练ID: {training_id}")
        return True
    except Exception as e:
        logging.error(f"提取并添加数据库注释失败: {str(e)}")
        return False

def main():
    # 默认配置
    default_config = {
        "ddl_file": "data/schema/table_all.sql",
        "doc_file": "",
        "extract_comments": False
    }
    
    parser = argparse.ArgumentParser(description='向Vanna添加数据库信息')
    parser.add_argument('--ddl-file', help='DDL文件路径')
    parser.add_argument('--doc-file', help='表文档文件路径')
    parser.add_argument('--extract-comments', action='store_true', help='从数据库提取注释')
    args = parser.parse_args()
    
    # 初始化日志
    setup_logging()
    
    # 创建数据库连接
    db_connection = DatabaseConnection()
    
    # 初始化Vanna，直接传入数据库连接
    llm_model = LLMFactory.create_llm()
    embedding_model = EmbeddingFactory.create_embedding()
    vanna_setup = VannaSetup(llm_model, embedding_model)
    vanna_instance = vanna_setup.initialize_vanna(db_connection=db_connection)
    
    success_count = 0
    
    # 优先使用默认配置，如果默认配置为空则使用命令行参数
    ddl_file = default_config["ddl_file"] if default_config["ddl_file"] else args.ddl_file
    doc_file = default_config["doc_file"] if default_config["doc_file"] else args.doc_file
    extract_comments = default_config["extract_comments"] if default_config["extract_comments"] else args.extract_comments
    
    # 添加DDL文件
    if ddl_file:
        if add_ddl_from_file(vanna_instance, ddl_file):
            success_count += 1
    
    # 添加表文档文件
    if doc_file:
        if add_documentation_from_file(vanna_instance, doc_file):
            success_count += 1
    
    # 从数据库提取注释
    if extract_comments:
        if extract_and_add_comments(vanna_instance, db_connection):
            success_count += 1
    
    if success_count > 0:
        logging.info(f"成功完成 {success_count} 项操作")
    else:
        logging.warning("未执行任何操作，请提供至少一个参数")
        parser.print_help()

if __name__ == "__main__":
    main()