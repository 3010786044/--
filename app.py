from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import logging
import json
import traceback

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = Flask(__name__)
# 允许所有来源的跨域请求
CORS(app, resources={r"/api/*": {"origins": "*"}})

def call_aliyun_api(question):
    try:
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        api_key = os.getenv('ALIYUN_API_KEY')
        logger.info(f"Using Aliyun API key: {api_key[:5]}...{api_key[-5:]}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            "parameters": {}
        }
        logger.info(f"Calling Aliyun API with question: {question}")
        logger.info(f"Headers: Authorization: Bearer {api_key[:5]}...{api_key[-5:]}, Content-Type: application/json")
        logger.info(f"Request data: {json.dumps(data)}")
        
        response = requests.post(url, headers=headers, json=data)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.text}")
        
        if response.status_code != 200:
            error_msg = f"API调用失败: HTTP {response.status_code}"
            logger.error(error_msg)
            return error_msg
            
        result = response.json()
        if 'output' not in result:
            error_msg = "API响应格式错误：缺少output字段"
            logger.error(error_msg)
            return error_msg
            
        logger.info("Successfully received response from Aliyun API")
        return result.get('output', {}).get('text', '')
    except requests.exceptions.RequestException as e:
        error_msg = f"请求异常: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"未知错误: {str(e)}"
        logger.error(error_msg)
        return error_msg

def call_kimi_api(question):
    try:
        url = "https://api.moonshot.cn/v1/chat/completions"
        api_key = os.getenv('KIMI_API_KEY')
        logger.info(f"Using Kimi API key: {api_key[:5]}...{api_key[-5:]}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "moonshot-v1-8k",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "temperature": 0.7
        }
        logger.info(f"Calling Kimi API with question: {question}")
        logger.info(f"Headers: Authorization: Bearer {api_key[:5]}...{api_key[-5:]}, Content-Type: application/json")
        logger.info(f"Request data: {json.dumps(data)}")
        
        response = requests.post(url, headers=headers, json=data)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.text}")
        
        if response.status_code != 200:
            error_msg = f"API调用失败: HTTP {response.status_code}"
            logger.error(error_msg)
            return error_msg
            
        result = response.json()
        if 'choices' not in result or not result['choices']:
            error_msg = "API响应格式错误：缺少choices字段或为空"
            logger.error(error_msg)
            return error_msg
            
        logger.info("Successfully received response from Kimi API")
        return result.get('choices', [{}])[0].get('message', {}).get('content', '')
    except requests.exceptions.RequestException as e:
        error_msg = f"请求异常: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"未知错误: {str(e)}"
        logger.error(error_msg)
        return error_msg

def call_deepseek_api(question):
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        api_key = os.getenv('DEEPSEEK_API_KEY')
        logger.info(f"Using DeepSeek API key: {api_key[:5]}...{api_key[-5:]}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
        logger.info(f"Calling DeepSeek API with question: {question}")
        logger.info(f"Headers: {headers}")
        logger.info(f"Data: {data}")
        response = requests.post(url, headers=headers, json=data)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.text}")
        response.raise_for_status()
        result = response.json()
        logger.info("Successfully received response from DeepSeek API")
        return result.get('choices', [{}])[0].get('message', {}).get('content', '')
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling DeepSeek API: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        error_msg = f"未知错误: {str(e)}"
        logger.error(error_msg)
        return error_msg

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    # 处理OPTIONS请求（预检请求）
    if request.method == 'OPTIONS':
        logger.info("Received OPTIONS request, responding with CORS headers")
        return '', 204
        
    try:
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request data (raw): {request.data}")
        
        # 记录请求内容类型
        content_type = request.headers.get('Content-Type', '')
        logger.info(f"Content-Type: {content_type}")
        
        # 尝试多种方式解析请求数据
        data = None
        
        # 直接尝试解析JSON
        try:
            data = request.get_json(force=True, silent=True)
            if data:
                logger.info(f"Request data (parsed json force=True): {data}")
        except Exception as e:
            logger.error(f"Error parsing JSON with force=True: {str(e)}")
            
        # 如果上面失败，尝试手动解析
        if not data and request.data:
            try:
                data = json.loads(request.data.decode('utf-8'))
                logger.info(f"Request data (decoded manually): {data}")
            except Exception as e:
                logger.error(f"Error decoding request data: {str(e)}")
                logger.error(f"Raw data: {request.data}")
                
                # 尝试修复可能的JSON格式问题
                try:
                    # 替换非标准的JSON格式
                    raw_data = request.data.decode('utf-8').replace("\\:", ":").replace("\\,", ",")
                    logger.info(f"Attempting to fix JSON: {raw_data}")
                    data = json.loads(raw_data)
                    logger.info(f"Fixed JSON parsing: {data}")
                except Exception as e2:
                    logger.error(f"Error fixing JSON: {str(e2)}")
        
        # 尝试从表单数据获取
        if not data and request.form:
            try:
                form_data = dict(request.form)
                logger.info(f"Form data: {form_data}")
                if 'question' in form_data:
                    data = form_data
            except Exception as e:
                logger.error(f"Error processing form data: {str(e)}")
        
        if not data:
            logger.error("No valid data received")
            return jsonify({"error": "无效的请求数据，请确保发送正确的JSON格式"}), 400

        question = data.get('question')
        model = data.get('model', 'aliyun')

        if not question:
            logger.error("Empty question received")
            return jsonify({"error": "问题不能为空"}), 400

        logger.info(f"Received question: {question}, model: {model}")

        if model == 'aliyun':
            answer = call_aliyun_api(question)
        elif model == 'kimi':
            answer = call_kimi_api(question)
        elif model == 'deepseek':
            answer = call_deepseek_api(question)
        else:
            logger.error(f"Unsupported model: {model}")
            return jsonify({"error": "不支持的模型"}), 400

        if answer.startswith("Error:") or answer.startswith("API调用失败:") or answer.startswith("请求异常:") or answer.startswith("未知错误:"):
            return jsonify({"error": answer}), 500

        return jsonify({"answer": answer})

    except Exception as e:
        error_msg = f"服务器内部错误: {str(e)}"
        stack_trace = traceback.format_exc()
        logger.error(error_msg)
        logger.error(f"Stack trace: {stack_trace}")
        return jsonify({"error": error_msg}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/')
def index():
    return jsonify({"message": "AI Chat API is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 