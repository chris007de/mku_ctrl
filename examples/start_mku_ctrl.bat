@echo off

call CD "C:\Users\user\miniconda3\Scripts"
call activate.bat mku
call CD "C:\Users\user\mku_ctrl"
call python mku_ctrl.py COM1