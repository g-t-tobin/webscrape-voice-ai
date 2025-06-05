FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg libsndfile1
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "voicebot.asgi:application"]
