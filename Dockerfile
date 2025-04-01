FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"] 