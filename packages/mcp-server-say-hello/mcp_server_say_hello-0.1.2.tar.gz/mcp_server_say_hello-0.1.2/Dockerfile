FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -U pip && pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "-m", "mcp_server_say_hello"]