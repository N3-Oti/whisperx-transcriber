# WhisperX実行スクリプト (PowerShell) - タイムスタンプ付き
# 使用方法: .\run_whisperx_with_timestamps.ps1

Write-Host "=== WhisperX 音声書き起こし開始（タイムスタンプ付き） ===" -ForegroundColor Green

# 出力ディレクトリを作成
if (!(Test-Path "output")) {
    New-Item -ItemType Directory -Path "output"
}

# audioディレクトリ内の音声ファイルを処理
$audioExtensions = @("*.mp3", "*.wav", "*.m4a", "*.flac")
$audioFiles = @()

foreach ($ext in $audioExtensions) {
    $audioFiles += Get-ChildItem -Path "audio" -Filter $ext -ErrorAction SilentlyContinue
}

if ($audioFiles.Count -eq 0) {
    Write-Host "audioディレクトリに音声ファイルが見つかりません" -ForegroundColor Yellow
    Write-Host "音声ファイルをaudioディレクトリに配置してください" -ForegroundColor Yellow
    exit
}

foreach ($audioFile in $audioFiles) {
    Write-Host "処理中: $($audioFile.Name)" -ForegroundColor Cyan
    
    # WhisperXで書き起こし実行（タイムスタンプ付き）
    # --output_format srt でSRT形式（タイムスタンプ付き）で出力
    docker run --gpus all -it `
        -v "${PWD}/audio:/app/audio" `
        -v "${PWD}/output:/app/output" `
        ghcr.io/jim60105/whisperx:large-v3-ja `
        -- --output_format srt --output_dir /app/output "/app/audio/$($audioFile.Name)"
    
    Write-Host "完了: $($audioFile.Name)" -ForegroundColor Green
}

Write-Host "=== 全ての処理が完了しました ===" -ForegroundColor Green
Write-Host "生成されたファイル:" -ForegroundColor Cyan
Get-ChildItem -Path "output" | Format-Table Name, Length, LastWriteTime 