@echo off
echo ========================================
echo GitHub 同步脚本
echo ========================================
echo.

REM 检查是否已配置远程仓库
git remote -v >nul 2>&1
if %errorlevel% equ 0 (
    echo 检测到远程仓库配置
    git remote -v
    echo.
    echo 正在推送到GitHub...
    git push -u origin main
    if %errorlevel% equ 0 (
        echo.
        echo ✅ 代码已成功推送到GitHub！
    ) else (
        echo.
        echo ❌ 推送失败，请检查：
        echo    1. 是否已创建GitHub仓库
        echo    2. 远程仓库地址是否正确
        echo    3. 是否有推送权限
    )
) else (
    echo 未检测到远程仓库配置
    echo.
    echo 请先执行以下步骤：
    echo.
    echo 1. 在GitHub上创建新仓库
    echo 2. 执行以下命令添加远程仓库：
    echo.
    echo    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
    echo.
    echo 3. 然后重新运行此脚本
    echo.
    echo 或者直接执行：
    echo    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
    echo    git branch -M main
    echo    git push -u origin main
)

echo.
pause
