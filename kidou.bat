@echo off
:: Windows Terminal (wt.exe) を管理者権限で起動してスクリプト実行
powershell -Command "Start-Process wt.exe -Verb RunAs -ArgumentList 'pwsh -NoExit -Command cd %~dp0; .\run_whisperx_complete.ps1'"

