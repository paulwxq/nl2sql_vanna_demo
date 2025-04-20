# main.py
"""
项目入口文件
"""
import logging
import argparse
import os
from app.config import LOGGING_CONFIG, LLM_CONFIG, EMBEDDING_CONFIG
from app.db.connection import DatabaseConnection
from app.langchain.llm_config import LLMFactory, EmbeddingFactory
from app.vanna.setup import VannaSetup
from app.vanna.query_processor import QueryProcessor

# 设置日志
def setup_logging():
    """设置日志配置"""
    log_dir = os.path.dirname(LOGGING_CONFIG['file'])
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG['level']),
        format=LOGGING_CONFIG['format'],
        filename=LOGGING_CONFIG['file'],
        filemode='a'
    )
    
    # 添加控制台处理器
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='NL2SQL Demo')
    parser.add_argument('--train', action='store_true', help='训练模式')
    parser.add_argument('--query', type=str, help='要处理的自然语言查询')
    args = parser.parse_args()
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("启动NL2SQL Demo应用")
    
    try:
        # 初始化数据库连接
        db_connection = DatabaseConnection()  # 尝试连接数据库，如果失败则抛出异常并退出
        
        # 初始化LLM和Embedding模型
        llm_model = LLMFactory.create_llm()
        embedding_model = EmbeddingFactory.create_embedding()
        
        # 设置Vanna
        vanna_setup = VannaSetup(llm_model, embedding_model)
        vanna_instance = vanna_setup.initialize_vanna()
        
        # 连接Vanna到数据库
        vanna_setup.connect_to_database(db_connection)
        
        # 初始化查询处理器
        query_processor = QueryProcessor(vanna_instance, db_connection)
        
        if args.train:
            logger.info("进入训练模式")
            # 这里可以添加训练逻辑
            # 例如加载训练数据并训练Vanna
            pass
            
        if args.query:
            # 处理单个查询
            result = query_processor.process_query(args.query)
            if result['success']:
                print(f"SQL查询: {result['sql']}")
                print("查询结果:")
                for row in result['results']:
                    print(row)
            else:
                print(f"查询错误: {result['error']}")
    
    except Exception as e:
        logger.error(f"应用错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()