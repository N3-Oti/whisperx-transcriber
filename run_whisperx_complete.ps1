# WhisperX完全自動実行スクリプト (PowerShell)
# 使用方法: .\run_whisperx_complete.ps1
# 書き起こし実行からテキスト変換まで一括で自動実行

# 全体の処理開始時間を記録
$totalStartTime = Get-Date

Write-Host "=== WhisperX 完全自動音声書き起こし開始 ===" -ForegroundColor Green
Write-Host "開始時刻: $($totalStartTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Cyan

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

Write-Host "処理対象ファイル数: $($audioFiles.Count)" -ForegroundColor Cyan

# Step 1: WhisperXで書き起こし実行
Write-Host "`n=== Step 1: WhisperX書き起こし実行 ===" -ForegroundColor Yellow
$whisperxStartTime = Get-Date

foreach ($audioFile in $audioFiles) {
    Write-Host "処理中: $($audioFile.Name)" -ForegroundColor Cyan
    $fileStartTime = Get-Date
    
    # WhisperXで書き起こし実行（タイムスタンプ付き）
    $whisperxResult = Measure-Command {
        docker run --gpus all -it `
            -v "${PWD}/audio:/app/audio" `
            -v "${PWD}/output:/app/output" `
            ghcr.io/jim60105/whisperx:large-v3-ja `
            -- --output_format srt --output_dir /app/output "/app/audio/$($audioFile.Name)"
    }
    
    $fileEndTime = Get-Date
    $fileDuration = $fileEndTime - $fileStartTime
    
    Write-Host "完了: $($audioFile.Name)" -ForegroundColor Green
    Write-Host "  処理時間: $($fileDuration.ToString('hh\:mm\:ss'))" -ForegroundColor Yellow
}

$whisperxEndTime = Get-Date
$whisperxDuration = $whisperxEndTime - $whisperxStartTime
Write-Host "`nWhisperX書き起こし総時間: $($whisperxDuration.ToString('hh\:mm\:ss'))" -ForegroundColor Magenta

# Step 2: SRTからテキスト形式に変換
Write-Host "`n=== Step 2: SRT→テキスト変換 ===" -ForegroundColor Yellow
$convertStartTime = Get-Date

# Pythonスクリプトを実行
$convertResult = Measure-Command {
    python convert_srt_to_text.py
}

$convertEndTime = Get-Date
$convertDuration = $convertEndTime - $convertStartTime
Write-Host "SRT→テキスト変換時間: $($convertDuration.ToString('hh\:mm\:ss'))" -ForegroundColor Magenta

# Step 3: 結果表示
Write-Host "`n=== Step 3: 処理結果 ===" -ForegroundColor Yellow

Write-Host "生成されたファイル:" -ForegroundColor Cyan
$outputFiles = Get-ChildItem -Path "output" | Sort-Object Name
foreach ($file in $outputFiles) {
    $fileSize = [math]::Round($file.Length / 1KB, 2)
    Write-Host "  - $($file.Name) ($fileSize KB)" -ForegroundColor White
}

Write-Host "`n=== 全ての処理が完了しました ===" -ForegroundColor Green
Write-Host "テキストファイルは 'output/' ディレクトリに保存されています" -ForegroundColor Cyan

# 全体の処理時間を計算・表示
$totalEndTime = Get-Date
$totalDuration = $totalEndTime - $totalStartTime

Write-Host "`n=== 処理時間サマリー ===" -ForegroundColor Green
Write-Host "開始時刻: $($totalStartTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Cyan
Write-Host "終了時刻: $($totalEndTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Cyan
Write-Host "WhisperX書き起こし時間: $($whisperxDuration.ToString('hh\:mm\:ss'))" -ForegroundColor Yellow
Write-Host "SRT→テキスト変換時間: $($convertDuration.ToString('hh\:mm\:ss'))" -ForegroundColor Yellow
Write-Host "総処理時間: $($totalDuration.ToString('hh\:mm\:ss'))" -ForegroundColor Magenta 