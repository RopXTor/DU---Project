import os

file_main = "main.py"

dir_path = os.path.dirname(__file__)
path = os.path.join(dir_path, file_main)

os.system('streamlit run "{}"'.format(path))
