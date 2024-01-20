@echo off
setlocal enabledelayedexpansion

REM Change directory to your project's root
cd D:\DJANGO\lab_django_project

REM Check for unstaged changes
git status
echo.
set /p "confirm=Do you wish to stage all changes and push to GitHub? (y/n): "
if /i "!confirm!" NEQ "y" exit /b

REM Stage all changes
git add .

REM Commit changes
set /p "commitMsg=Enter your commit message: "
git commit -m "!commitMsg!"

REM Push to remote repository
git push -u origin master

echo.
echo Changes have been pushed to GitHub.
pause
