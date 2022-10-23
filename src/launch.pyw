import os
import codecs
from getpass import getuser

os.chdir(f"C:\\Users\\{getuser()}\\AppData\\Local\\Temp")

exec(codecs.open("app.py", "r", "utf-8").read())