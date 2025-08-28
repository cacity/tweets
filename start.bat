@echo off
echo 启动Twitter RSS订阅管理器 Web应用...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 尝试安装依赖
echo 正在检查并安装依赖...
pip install Flask requests feedparser python-dateutil

REM 启动Flask应用
echo.
echo 启动Web应用...
echo 应用将在 http://127.0.0.1:5000 运行
echo 按 Ctrl+C 停止服务器
echo.
python app.py

pause