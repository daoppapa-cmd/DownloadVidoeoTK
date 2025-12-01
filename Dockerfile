FROM python:3.9-slim

# ដំឡើង ffmpeg (សំខាន់សម្រាប់ yt-dlp ដំណើរការល្អ)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "tiktok_bot.py"]
