FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 7860

CMD ["python", "-m", "streamlit", "run", "chatbot/app.py", \
     "--server.port=7860", \
     "--server.address=0.0.0.0"]
