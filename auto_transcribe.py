#!/usr/bin/env python3
"""
自動音声書き起こしスクリプト
コンテナ起動時にaudioディレクトリ内のファイルを自動で書き起こし
"""

import os
import sys
import whisper
import logging
import time
import threading
from pathlib import Path
from tqdm import tqdm

def setup_logging():
    """ログ設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def format_timestamp(seconds):
    """
    秒数を HH:MM:SS 形式に変換
    
    Args:
        seconds (float): 秒数
        
    Returns:
        str: フォーマットされたタイムスタンプ
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def update_progress_bar(pbar, stop_event):
    """
    プログレスバーをリアルタイムで更新
    
    Args:
        pbar: tqdmプログレスバーオブジェクト
        stop_event: 停止イベント
    """
    start_time = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        pbar.n = int(elapsed)
        pbar.set_postfix({"経過時間": f"{elapsed:.1f}s"})
        pbar.refresh()
        time.sleep(0.5)  # 0.5秒ごとに更新

def transcribe_file(input_path, model, model_name, logger):
    """
    音声ファイルを書き起こし
    
    Args:
        input_path (str): 入力ファイルのパス
        model: Whisperモデル
        model_name (str): モデル名
        logger: ロガーオブジェクト
        
    Returns:
        str: 出力ファイルのパス
    """
    try:
        # 出力ファイル名を生成（モデル名付き）
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(
            "/app/output",
            f"{base_name}_{model_name}_transcript.txt"
        )
        
        logger.info(f"書き起こし開始: {os.path.basename(input_path)} (モデル: {model_name})")
        
        # プログレスバーを作成
        with tqdm(
            desc=f"書き起こし中: {os.path.basename(input_path)} ({model_name})",
            unit="秒",
            leave=True
        ) as pbar:
            # 停止イベントを作成
            stop_event = threading.Event()
            
            # 進捗更新スレッドを開始
            progress_thread = threading.Thread(
                target=update_progress_bar, 
                args=(pbar, stop_event)
            )
            progress_thread.start()
            
            try:
                # 書き起こし実行
                result = model.transcribe(
                    input_path, 
                    language="ja",
                    verbose=False
                )
            finally:
                # 進捗更新を停止
                stop_event.set()
                progress_thread.join()
            
            # 完了状態を表示
            pbar.set_postfix({"完了": "✅"})
            pbar.refresh()
        
        # タイムスタンプ付きの結果を整形
        transcriptions = []
        for segment in result["segments"]:
            start_time = format_timestamp(segment["start"])
            text = segment["text"].strip()
            transcriptions.append(f"[{start_time}] {text}")
        
        # 結果をファイルに保存
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in transcriptions:
                f.write(line + '\n')
        
        logger.info(f"書き起こし完了: {output_path}")
        return output_path
                
    except Exception as e:
        logger.error(f"ファイル処理に失敗しました: {input_path} - {e}")
        raise

def main():
    logger = setup_logging()
    
    # ディレクトリパス
    audio_dir = "/app/audio"
    output_dir = "/app/output"
    
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info("=== 自動音声書き起こし開始 ===")
    
    # 音声ファイルの拡張子
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac']
    
    # audioディレクトリ内の音声ファイルを検索
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(Path(audio_dir).glob(f"*{ext}"))
    
    if not audio_files:
        logger.info("audioディレクトリに音声ファイルが見つかりません")
        logger.info("音声ファイルをaudioディレクトリに配置してください")
        return
    
    logger.info(f"処理対象ファイル数: {len(audio_files)}")
    
    # Whisperモデルを読み込み（largeモデルに変更）
    model_name = "large"
    logger.info(f"Whisperモデル '{model_name}' を読み込み中...")
    model = whisper.load_model(model_name)
    logger.info("モデルの読み込みが完了しました")
    
    # 各ファイルを処理
    for audio_file in audio_files:
        try:
            logger.info(f"処理中: {audio_file.name}")
            transcribe_file(str(audio_file), model, model_name, logger)
        except Exception as e:
            logger.error(f"エラーが発生しました: {audio_file.name} - {e}")
            continue
    
    logger.info("=== 全ての処理が完了しました ===")
    
    # 処理結果の表示
    output_files = list(Path(output_dir).glob("*.txt"))
    if output_files:
        logger.info("生成されたファイル:")
        for output_file in output_files:
            logger.info(f"  - {output_file.name}")

if __name__ == "__main__":
    main() 