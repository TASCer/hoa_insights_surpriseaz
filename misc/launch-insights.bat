cd /D "D:\PycharmProjects\hoa_insights_surpriseaz\src"
echo %cd%
call conda activate hoa_insights_surpriseaz
python.exe "main.py"
if NOT ["%errorlevel%"] == ["0"] pause