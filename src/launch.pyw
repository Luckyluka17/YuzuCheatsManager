import os
from getpass import getuser

os.chdir(f"C:\\Users\\{getuser()}\\AppData\\Local\\Temp\\YuzuCheatsManager")

exec(open("app.py", "r", encoding="utf-8").read())