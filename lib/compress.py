#!/usr/bin/env python
import os
from subprocess import call #shell out to pdftk

f = []
mypath = "./tmp/"
for (dirpath, dirnames, filenames) in os.walk(mypath):
    f.extend(filenames)
    break

print(f)
for file_ in f:
    if os.path.splitext(file_)[1] == ".pdf":
        print file_
        call("gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dBATCH  -dQUIET -sOutputFile=compress/" + file_ + " tmp/" + file_, shell=True)