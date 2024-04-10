@echo off

set /p file=json文件:

for %%i in (%file%) do set dirname=%%~dpi

echo 拿到文件%file%

dsanimtool "%file%" "%dirname%/"

echo 已执行dsanimtool,生成同名zip文件

set zipfile=%dirname%
set suffix=".zip"
::echo 请将生成的%zipfile%%suffix%文件移动到 workshop\content\322330\3052181004\anim 下

pause