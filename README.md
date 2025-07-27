# WhisperX 音声書き起こしシステム

WhisperXを使用して音声ファイル（MP3、WAV、M4A、FLAC）をタイムスタンプ付きで書き起こすシステムです。

## 特徴

- ✅ **WhisperX使用**: 高精度な音声認識とタイムスタンプ
- ✅ **タイムスタンプ形式**: `[H:MM:SS - H:MM:SS]` 形式
- ✅ **Docker対応**: 環境構築不要で簡単実行
- ✅ **複数形式対応**: MP3、WAV、M4A、FLAC
- ✅ **自動処理**: ディレクトリ内の全音声ファイルを一括処理

## 必要な環境

- Docker Desktop
- PowerShell（Windows）または Bash（Linux/Mac）

## セットアップ

### 1. Docker Desktopのインストールと起動

#### Windows
1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)をダウンロード
2. インストーラーを実行し、インストール完了後Docker Desktopを起動
3. WSL2の有効化が必要な場合は、インストーラーの指示に従って設定

#### macOS
1. [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)をダウンロード
2. インストーラーを実行し、インストール完了後Docker Desktopを起動

#### Linux (Ubuntu)
```bash
# Docker Engineのインストール
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# ユーザーをdockerグループに追加（再ログインが必要）
sudo usermod -aG docker $USER

# Dockerサービスの起動
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. WhisperX Dockerイメージの確認

初回実行時に自動的にDockerイメージがダウンロードされますが、事前に確認したい場合は：

```powershell
# PowerShell
docker pull ghcr.io/jim60105/whisperx:large-v3-ja

# または Linux/Mac
docker pull ghcr.io/jim60105/whisperx:large-v3-ja
```

### 3. 音声ファイルの準備

音声ファイルを`audio/`ディレクトリに配置してください。

## 使用方法

### 1. 音声ファイルの準備

音声ファイルを`audio/`ディレクトリに配置してください：
```
audio/
├── sample1.mp3
├── sample2.wav
└── sample3.m4a
```

### 2. 一括実行（推奨）

書き起こし実行からテキスト変換まで一括で自動実行：

```powershell
.\run_whisperx_complete.ps1
```

### 3. 個別実行

#### 書き起こし実行のみ

```powershell
.\run_whisperx_with_timestamps.ps1
```

#### テキスト形式への変換のみ

```powershell
python convert_srt_to_text.py
```

## 出力ファイル

処理後、`output/`ディレクトリに以下のファイルが生成されます：

- `{ファイル名}.srt` - WhisperXが生成したSRT形式の字幕ファイル
- `{ファイル名}_with_timestamps.txt` - 変換後のテキストファイル

### 出力例

```
=== WhisperX 書き起こし結果 ===
入力ファイル: sample.mp3
モデル: large-v3-ja
タイムスタンプ形式: [H:MM:SS - H:MM:SS]
==================================================

[0:00:04 - 0:00:30]
録画を開始しましたこれ先週の畳み込みの長所は何ですかと先週

[0:00:30 - 0:00:45]
局所的なものを見ながら行くのでそういう局所的な関係が強いというような画像データとかに関してはすごく異性度が出ますよという話をしました
```

## ファイル構成

```
mp4-md/
├── audio/                           # 入力音声ファイル
├── output/                          # 出力ファイル
├── run_whisperx_complete.ps1        # 一括実行スクリプト（推奨）
├── run_whisperx_with_timestamps.ps1 # 個別実行スクリプト
├── convert_srt_to_text.py           # SRT→テキスト変換スクリプト
├── .gitignore
└── README.md
```

## 技術仕様

- **WhisperXモデル**: large-v3-ja
- **Dockerイメージ**: ghcr.io/jim60105/whisperx:large-v3-ja
- **対応音声形式**: MP3、WAV、M4A、FLAC
- **出力形式**: SRT（中間）、テキスト（最終）
- **タイムスタンプ**: [H:MM:SS - H:MM:SS]形式

## トラブルシューティング

### Docker Desktopが起動していない場合
```
error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping"
```
→ Docker Desktopを起動してください。

### Dockerイメージのダウンロードエラー
```
Unable to find image 'ghcr.io/jim60105/whisperx:large-v3-ja' locally
```
→ 初回実行時は自動的にダウンロードされます。ネットワーク接続を確認してください。

### 音声ファイルが見つからない場合
```
audioディレクトリに音声ファイルが見つかりません
```
→ `audio/`ディレクトリに音声ファイルを配置してください。

### GPUエラーが発生する場合
→ CPUでも動作しますが、処理時間が長くなります。

### Docker権限エラー（Linux）
```
Got permission denied while trying to connect to the Docker daemon socket
```
→ ユーザーをdockerグループに追加し、再ログインしてください：
```bash
sudo usermod -aG docker $USER
# 再ログイン後
newgrp docker
```

## 参考・引用

### 使用している技術・ライブラリ

#### WhisperX
- **GitHub**: [m-bain/whisperX](https://github.com/m-bain/whisperX)
- **説明**: 高精度な音声認識とタイムスタンプ機能を提供するWhisperXライブラリ

#### Dockerイメージ
- **GitHub**: [jim60105/docker-whisperX](https://github.com/jim60105/docker-whisperX)
- **Docker Hub**: `ghcr.io/jim60105/whisperx:large-v3-ja`
- **説明**: WhisperXをDockerコンテナで簡単に実行できるようにしたイメージ

### 謝辞
このプロジェクトは、上記のオープンソースプロジェクトを基に構築されています。開発者の皆様に感謝いたします。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 