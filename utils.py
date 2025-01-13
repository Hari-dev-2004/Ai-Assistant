# utils.py

import os

def delete_file(filename):
    try:
        os.remove(filename)
    except Exception as e:
        print(f"Error deleting file {filename}: {e}")
