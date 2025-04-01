from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://9999999.xin", "http://9999999.xin"]}})

# 配置API密钥
ALIYUN_API_KEY = os.getenv('ALIYUN_API_KEY')
KIMI_API_KEY = os.getenv('KIMI_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

def call_aliyun_api(question):
    response = requests.post(
        'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
        headers={
            'Authorization': f'Bearer {ALIYUN_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'qwen-turbo',
            'input': {
                'messages': [{'role': 'user', 'content': question}]
            }
        }
    )
    if response.status_code == 200:
        result = response.json()
        return result['output']['text']
    return None

def call_kimi_api(question):
    response = requests.post(
        'https://api.moonshot.cn/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {KIMI_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'moonshot-v1-8k',
            'messages': [{'role': 'user', 'content': question}]
        }
    )
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    return None

def call_deepseek_api(question):
    response = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': question}]
        }
    )
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    return None

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question')
        model = data.get('model', 'aliyun')  # 默认使用阿里云模型
        
        if not question:
            return jsonify({'error': '问题不能为空'}), 400

        answer = None
        if model == 'aliyun':
            answer = call_aliyun_api(question)
        elif model == 'kimi':
            answer = call_kimi_api(question)
        elif model == 'deepseek':
            answer = call_deepseek_api(question)

        if answer:
            return jsonify({'answer': answer})
        else:
            return jsonify({'error': 'API调用失败'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 