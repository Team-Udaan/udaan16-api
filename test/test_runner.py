from sys import stdout
import subprocess
from os import path
from os import listdir


test_folder_path = path.dirname(__file__)

files = [f for f in listdir(test_folder_path) if path.isfile(path.join(test_folder_path, f))]

test_files = [
    "test.testbase",
    "test.handle",
    "test.testreport",
]

# test_files = ["test." + f.strip(".py") for f in files if not f.startswith("_")]

for f in test_files:
    subprocess.check_output(["python3.4", "-m", "unittest", f], stderr=stdout)