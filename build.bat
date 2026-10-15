@echo off
echo Building MedyaIndirici...
pyinstaller --noconfirm --onedir --windowed --icon="icon3.ico" --add-data="icon3.ico;." --name "MedyaIndirici" main.py
echo Build finished!
pause
