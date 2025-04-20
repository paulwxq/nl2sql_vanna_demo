# web/app.py
"""
Web应用入口
"""
import logging
import sys
import os

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from app.db.connection import DatabaseConnection
from app.vanna.setup import VannaSetup
from app.langchain.llm_config import LLMFactory, EmbeddingFactory
from app.vanna.query_processor import QueryProcessor
from app.vanna.trainer import VannaTrainer
from app.schemas.request import NLQueryRequest, FeedbackRequest, TrainingRequest

logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS

# 初始化组件
db_connection = DatabaseConnection()  # 尝试连接数据库，如果失败则抛出异常并退出
llm_model = LLMFactory.create_llm()
embedding_model = EmbeddingFactory.create_embedding()
vanna_setup = VannaSetup(llm_model, embedding_model)
vanna_instance = vanna_setup.initialize_vanna()
vanna_setup.connect_to_database(db_connection)
query_processor = QueryProcessor(vanna_instance, db_connection)
trainer = VannaTrainer(vanna_instance)

@app.route('/')
def index():
    """提供主页"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def handle_query():
    """处理查询请求"""
    try:
        data = request.json
        query_request = NLQueryRequest(**data)
        
        result = query_processor.process_query(query_request.question)
        return jsonify(result)
    except Exception as e:
        logger.error(f"处理查询请求错误: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/api/feedback', methods=['POST'])
def handle_feedback():
    """处理反馈请求"""
    try:
        data = request.json
        feedback_request = FeedbackRequest(**data)
        
        success = query_processor.train_from_feedback(
            feedback_request.question,
            feedback_request.sql,
            feedback_request.is_correct
        )
        
        return jsonify({
            "success": success,
            "message": "反馈已处理" if success else "处理反馈时出错"
        })
    except Exception as e:
        logger.error(f"处理反馈请求错误: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/api/train', methods=['POST'])
def handle_train():
    """处理训练请求"""
    try:
        data = request.json
        training_request = TrainingRequest(**data)
        
        response = trainer.train_single_item(training_request)
        return jsonify(response.dict())
    except Exception as e:
        logger.error(f"处理训练请求错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"训练失败: {str(e)}",
            "training_data_id": None
        }), 400

def run_app(host='0.0.0.0', port=5000, debug=False):
    """运行Flask应用"""
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_app(debug=True)