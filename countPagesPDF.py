#!/usr/bin/env python3
# Author: Rasmus Pettersson Vik
# Version: 1.0.1

import argparse
import sys
import os
from os import walk
import PyPDF2


def main(argv):
    parser = argparse.ArgumentParser(description="Counts the number of pages in PDF files")
    parser.add_argument("-r", "--recurse", action="store_true", help="Recursively find files in subdirectories")
    parser.add_argument("-t", "--total", action="store_true", help="Only print total count")
    parser.add_argument("-i", "--dir", type=str, help="Use another directory rather than the current working dir", default=os.getcwd())
    args = parser.parse_args()

    dir = args.dir
    files = []

    if not os.path.isdir(dir):
        print(f"ERROR - Path [{dir}] doesn't exist.", file=sys.stderr)
        return 1

    for (dirpath, dirnames, filenames) in walk(dir):
        for file in filenames:
            if file[-3:] == "pdf":
                files.append(f"{dirpath}{os.path.sep}{file}")
        if not args.recurse: #Break on first to not go into deeper folders
            break
    
    if len(files) == 0:
        print("No files found")
        return 0

    total = 0
    if not args.total:
        print("Pages\tFile")

    for file in files:
        try:
            with open(file, 'rb') as pdf:
                current = len(PyPDF2.PdfFileReader(file, strict=False).pages)
                total += current
                if not args.total:
                    print(f"{current}\t{file}")
        except IOError as e:
            print(e, file=sys.stderr)
    print(total)

if __name__ == '__main__':
    main(sys.argv)
