from sys import stdout
import subprocess
from os import path
from os import listdir


test_folder_path = path.dirname(__file__)

files = [f.rstrip(".py") for f in listdir(test_folder_path) if path.isfile(path.join(test_folder_path, f))]

files.remove("__init__")
files.remove("test_runner")

for f in files:
    subprocess.check_output(["python3.4", "-m", "unittest", f], stderr=stdout)
