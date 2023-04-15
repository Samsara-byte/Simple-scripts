"""
This code defines a Python function called find_epub_files that takes a single argument path.
The function uses the glob and os modules to find all files with the extension 
.epub within a given directory and its subdirectories.

Specifically, the glob.iglob() function is used to recursively search the path directory 
for all files with the .epub extension. The resulting file paths are added to a list called epub_files.

The function then creates a new file called novel_files.txt and writes the names of all 
.epub files found in the path directory and its subdirectories to this file, one file name per line.

Overall, this code is used to find and list all EPUB files within a specific directory and its subdirectories,
and store the list in a text file called novel_files.txt.
"""

import glob   # module for searching files
import os     # module for interacting with the operating system

def find_epub_files(path):
    epub_files = []   # create an empty list to store the names of epub files
    for file in glob.iglob(f'{path}/**/*.epub', recursive=True):
        # use glob.iglob() to find all files in path and its subdirectories with a .epub extension
        epub_files.append(os.path.basename(file))  
        # add the basename of the file to the list of epub files

    with open('novel_files.txt', 'w') as f:
        # create a new file called novel_files.txt and open it in write mode
        for file in epub_files:
            f.write(f'{file}\n')  # write each file name to the file, followed by a newline character

# call the function with the path of the directory to search for epub files
find_epub_files('/home/kadim/Lightnovels')

