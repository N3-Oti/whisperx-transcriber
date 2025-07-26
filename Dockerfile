FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    python3-tk \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*  

RUN pip install --upgrade pip
COPY requirements.txt /root/
WORKDIR /root/
RUN pip install -r requirements.txt

# 作業ディレクトリを作成
RUN mkdir -p /app
WORKDIR /app

# 自動実行スクリプトをコピー
COPY auto_transcribe.py /app/

# コンテナ起動時に自動実行
CMD ["python", "/app/auto_transcribe.py"] 