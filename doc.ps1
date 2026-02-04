# 1. 设置环境变量，确保 Python 全程 UTF-8
$env:PYTHONUTF8 = 1

# 2. 准备目录
New-Item -ItemType Directory -Force -Path "docs/api"

# 3. 如果没有首页，创建一个 (ASCII 安全版)
if (!(Test-Path "docs/index.md")) {
    "# Project Home`n`nWelcome to the API documentation." | Out-File -Encoding utf8 "docs/index.md"
}

# 4. 直接用 Python 的二进制流保存文件
# 逻辑：启动 pydoc-markdown，抓取它的原始字节输出(stdout)，直接写进 docs/api/app.md
Write-Host "Syncing API documentation..." -ForegroundColor Cyan

uv run python -c "import subprocess; res = subprocess.run(['pydoc-markdown', 'pydoc-markdown.yml'], capture_output=True); open('docs/api/app.md', 'wb').write(res.stdout)"

Write-Host "Success: API docs generated with binary-safe UTF-8!" -ForegroundColor Green

# 5. 启动预览
uv run mkdocs serve