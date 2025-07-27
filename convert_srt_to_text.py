#!/usr/bin/env python3
"""
SRT形式の字幕ファイルをテキスト形式に変換するスクリプト
"""

import os
import re
from pathlib import Path

def srt_time_to_timestamp(srt_time):
    """SRT時間形式 (HH:MM:SS,mmm) を H:MM:SS 形式に変換"""
    # SRT形式: 00:01:30,500 -> H:MM:SS
    time_parts = srt_time.replace(',', '.').split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(float(time_parts[2]))
    return f"{hours}:{minutes:02d}:{seconds:02d}"

def convert_srt_to_text(srt_file, text_file):
    """SRTファイルをテキスト形式に変換"""
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # SRTファイルの構造を解析
    # 1. 番号
    # 2. 時間 (00:01:30,500 --> 00:01:35,000)
    # 3. テキスト
    # 4. 空行
    
    # 時間行を検出して変換
    def replace_timestamp(match):
        start_time = match.group(1)
        end_time = match.group(2)
        start_timestamp = srt_time_to_timestamp(start_time)
        end_timestamp = srt_time_to_timestamp(end_time)
        return f"[{start_timestamp} - {end_timestamp}]"
    
    # 時間行を変換
    formatted_content = re.sub(
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})',
        replace_timestamp,
        content
    )
    
    # 番号行と空行を削除し、チャンクごとに改行を追加
    lines = formatted_content.split('\n')
    text_lines = []
    current_chunk = []
    
    for line in lines:
        line = line.strip()
        # 番号行（数字のみ）をスキップ
        if re.match(r'^\d+$', line):
            continue
        # 空行をスキップ
        if not line:
            continue
        # 時間行（既に変換済み）は新しいチャンクの開始
        if line.startswith('[') and line.endswith(']'):
            # 前のチャンクがあれば追加
            if current_chunk:
                text_lines.extend(current_chunk)
                text_lines.append('')  # チャンク間に空行を追加
            current_chunk = [line]
        # テキスト行
        else:
            current_chunk.append(line)
    
    # 最後のチャンクを追加
    if current_chunk:
        text_lines.extend(current_chunk)
    
    # ヘッダーを追加
    header = f"=== WhisperX 書き起こし結果 ===\n"
    header += f"入力ファイル: {os.path.basename(srt_file)}\n"
    header += f"モデル: large-v3-ja\n"
    header += f"タイムスタンプ形式: [H:MM:SS - H:MM:SS]\n"
    header += "=" * 50 + "\n\n"
    
    final_content = header + '\n'.join(text_lines)
    
    # 出力ファイルに保存
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"変換完了: {srt_file} -> {text_file}")

def main():
    """メイン処理"""
    output_dir = Path("output")
    
    # outputディレクトリ内の.srtファイルを処理
    srt_files = list(output_dir.glob("*.srt"))
    
    if not srt_files:
        print("outputディレクトリに.srtファイルが見つかりません")
        return
    
    print("=== SRT to Text 変換開始 ===")
    
    for srt_file in srt_files:
        output_file = srt_file.parent / f"{srt_file.stem}_with_timestamps.txt"
        print(f"処理中: {srt_file.name}")
        convert_srt_to_text(srt_file, output_file)
    
    print("=== 全ての変換が完了しました ===")
    print("生成されたファイル:")
    for file in output_dir.glob("*_with_timestamps.txt"):
        print(f"  - {file.name}")

if __name__ == "__main__":
    main() 