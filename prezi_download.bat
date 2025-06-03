@echo off
REM Prezi Downloader - Windows Batch Script
REM Usage: prezi_download.bat <prezi_url> [options]

if "%1"=="" (
    echo Usage: prezi_download.bat ^<prezi_url^> [options]
    echo.
    echo Examples:
    echo   prezi_download.bat https://prezi.com/p/example-presentation/
    echo   prezi_download.bat https://prezi.com/p/example/ --output my_output
    echo.
    echo For full options, run: uv run cli.py --help
    exit /b 1
)

echo Starting Prezi Downloader...
uv run cli.py %*
