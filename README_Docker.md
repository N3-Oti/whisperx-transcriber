# Docker GPU対応 Whisper 音声書き起こし環境

[Zennの記事](https://zenn.dev/yuarth/articles/dc81a0fa15748b)を参考に、DockerでGPU対応のWhisper環境を構築し、MP3をテキスト化するスクリプトを実行できるようにしました。

## 🐳 環境構成

```
mp4-md/
├── audio/                    # 音声ファイル配置ディレクトリ
├── output/                   # 書き起こし結果出力ディレクトリ
├── Dockerfile               # GPU対応Docker環境
├── docker-compose.yml       # Docker Compose設定
├── requirements.txt         # Python依存関係
├── transcribe_docker.py     # 音声書き起こしスクリプト
└── README_Docker.md         # このファイル
```

## 🚀 セットアップ手順

### 1. **音声ファイルを配置**
```bash
# audioディレクトリに音声ファイルを配置
cp your_audio.mp3 audio/
```

### 2. **Dockerコンテナをビルド・起動**
```bash
# コンテナをビルドして起動
docker-compose up -d
```

### 3. **コンテナに入る**
```bash
# コンテナに接続
docker exec -it whisper-gpu bash
```

## 📝 使用方法

### **基本的な書き起こし**
```bash
# コンテナ内で実行
python transcribe_docker.py sample.mp3
```

### **モデルを指定して書き起こし**
```bash
# 高精度モデル
python transcribe_docker.py sample.mp3 --model large

# 高速モデル
python transcribe_docker.py sample.mp3 --model turbo
```

### **複数ファイルの一括処理**
```bash
# 複数の音声ファイルを処理
for file in audio/*.mp3; do
    python transcribe_docker.py $(basename $file)
done
```

## 📁 ファイル配置

### **入力ファイル**
- `audio/` ディレクトリに音声ファイルを配置
- 対応形式: `.mp3`, `.wav`, `.m4a`, `.flac`

### **出力ファイル**
- `output/` ディレクトリに書き起こし結果が保存
- ファイル名: `{元ファイル名}_transcript.txt`

## ⚙️ 設定オプション

### **使用可能なモデル**
- `tiny`: 最も高速、低精度
- `base`: バランス型
- `small`: 中精度
- `medium`: 高精度
- `large`: 最高精度、低速
- `turbo`: 高速処理（デフォルト）

### **GPU確認**
```bash
# コンテナ内でGPU確認
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

## 🔧 トラブルシューティング

### **GPUが認識されない場合**
1. NVIDIA Docker Runtimeがインストールされているか確認
2. `nvidia-smi` でGPUが認識されているか確認
3. Docker ComposeのGPU設定を確認

### **メモリ不足の場合**
- より小さいモデル（`tiny`, `base`）を使用
- 大きな音声ファイルは分割して処理

## 📊 パフォーマンス

### **処理時間の目安（RTX 4080）**
- **tiny**: 1分の音声 ≈ 5-10秒
- **base**: 1分の音声 ≈ 10-20秒
- **turbo**: 1分の音声 ≈ 15-30秒
- **large**: 1分の音声 ≈ 30-60秒

## 🛠️ カスタマイズ

### **新しいモデルの追加**
`transcribe_docker.py` の `choices` リストに新しいモデルを追加

### **出力形式の変更**
`transcribe_docker.py` の `format_timestamp` 関数を修正

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。 