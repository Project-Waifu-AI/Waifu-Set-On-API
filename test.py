import os

# Mendapatkan current working directory
current_directory = os.getcwd()
print("Current Directory:", current_directory)

# Mendapatkan absolute path dari file
file_name = "test.py"
file_path = os.path.abspath(file_name)
print("Absolute Path of File:", file_path)
