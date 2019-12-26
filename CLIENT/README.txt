To install the libraries please execute this commandline:

	pip3 install -r requirements.txt



(For Windows OS): If you want to compile target.py to an executable file (.exe) you need to install PyInstaller

 with the command : pip3 install PyInstaller

 then run the command :          pyinstaller --onefile --noconsole target.py

 if it doesn't work correctly please compile it with this command : pyinstaller --onefile --windowed target.py