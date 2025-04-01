<?php
// 设置允许跨域访问
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');

// 处理预检请求
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// 只处理POST请求
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => '只接受POST请求']);
    exit;
}

// 开启错误日志
error_log("收到API代理请求: " . date('Y-m-d H:i:s'));

// 读取POST数据
$post_data = file_get_contents('php://input');
error_log("原始请求数据: " . $post_data);
$data = json_decode($post_data, true);

// 验证数据
if (!$data || !isset($data['question']) || !isset($data['model'])) {
    error_log("请求数据无效!");
    http_response_code(400);
    echo json_encode(['error' => '请求数据无效']);
    exit;
}

// 记录请求信息
error_log("请求问题: " . $data['question']);
error_log("使用模型: " . $data['model']);

// 设置API URL
$api_url = 'http://localhost:5000/api/chat';
error_log("转发到API: " . $api_url);

// 创建一个cURL句柄
$ch = curl_init($api_url);

// 设置cURL选项
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

// 执行cURL请求
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
error_log("API返回状态码: " . $http_code);

// 检查错误
if (curl_errno($ch)) {
    $error = "API请求失败: " . curl_error($ch);
    error_log($error);
    http_response_code(500);
    echo json_encode(['error' => $error]);
    exit;
}

// 关闭cURL句柄
curl_close($ch);

// 记录响应
error_log("API响应: " . $response);

// 转发API响应
http_response_code($http_code);
echo $response; 