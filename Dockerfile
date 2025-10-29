FROM python:3.12-slim
RUN pip install uv

COPY config/requirements.txt .

RUN uv pip install --system -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "-u", "main.py"]
