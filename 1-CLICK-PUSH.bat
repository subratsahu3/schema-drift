@echo off
title Push schema-drift to GitHub - @subratsahu3
echo ========================================================
echo   Pushing schema-drift to GitHub (@subratsahu3)
echo ========================================================
cd /d "%~dp0"
git branch -M main
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [NOTICE] Remote repository not found on GitHub.
    echo Opening your browser to create the empty repository...
    start https://github.com/new?name=schema-drift^&description=Polyglot+AST+Interface+and+Wire-Protocol+Consistency+Validator
    echo.
    echo 1. Click 'Create repository' in your browser.
    echo 2. Press any key below to complete the push!
    pause
    git push -u origin main
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   [SUCCESS] Code published to https://github.com/subratsahu3/schema-drift!
    echo ========================================================
)
pause
