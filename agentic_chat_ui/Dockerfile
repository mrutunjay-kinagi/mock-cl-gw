# agentic_chat_ui/Dockerfile

FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install streamlit requests

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
