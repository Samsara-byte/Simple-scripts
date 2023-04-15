"""
This is a Python code used to copy a specific file ("02.jpg") 
from a source directory ("/media/dalek/who/SİLİNECEKLER/One-Piece-Renkli") 
to a destination directory ("/home/dalek/Hard-Diskime-koyacaklarım/Kapak-Hikayeleri/toplu").
If there are multiple files with the same name, the code renames them with a numeric suffix to avoid overwriting.
The os and shutil modules are used to perform file operations such as checking if a file exists,
constructing file paths, and copying files.
"""


import os
import shutil

# Define the name of the files you want to copy
filename = "02.jpg"

# Define the source and destination directories
source_dir = "/media/dalek/who/SİLİNECEKLER/One-Piece-Renkli"
dest_dir = "/home/dalek/Hard-Diskime-koyacaklarım/Kapak-Hikayeleri/toplu"

# Initialize a counter to rename files with the same name
counter = 0

# Recursively search through the source directory to find the files
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file == filename:
            # Construct the full path of the source and destination files
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            # If the destination file already exists, rename it with a suffix
            while os.path.exists(dest_file):
                counter += 1
                dest_file = os.path.join(dest_dir, f"{os.path.splitext(file)[0]}_{counter:03d}{os.path.splitext(file)[1]}")
            # Copy the file to the destination directory
            shutil.copy(src_file, dest_file)
