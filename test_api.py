import requests
import json

def test_aliyun_api():
    url = "http://8.137.115.81:5000/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "question": "你好，世界！",
        "model": "aliyun"
    }
    
    print(f"发送请求到 {url}")
    print(f"请求头: {headers}")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if "answer" in result:
                print(f"回答: {result['answer']}")
            else:
                print(f"错误: 响应中没有answer字段")
        else:
            print(f"错误: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"请求异常: {str(e)}")

def test_kimi_api():
    url = "http://8.137.115.81:5000/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "question": "你好，世界！",
        "model": "kimi"
    }
    
    print(f"发送请求到 {url}")
    print(f"请求头: {headers}")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if "answer" in result:
                print(f"回答: {result['answer']}")
            else:
                print(f"错误: 响应中没有answer字段")
        else:
            print(f"错误: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"请求异常: {str(e)}")

if __name__ == "__main__":
    print("测试阿里云API:")
    test_aliyun_api()
    
    print("\n测试Kimi API:")
    test_kimi_api() 