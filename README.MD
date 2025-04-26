Steps to run install_tools.py

Create a new virtual environment inside D:\automations:

python -m venv .venv
Activate the virtual environment:


.\.venv\Scripts\activate
Install pyinstaller inside the venv:


pip install pyinstaller
Run PyInstaller:


pyinstaller --onefile --icon=path\to\icon\favicon.ico install_tools.py

To test if locally , run : python xxx.py    
