#!/usr/bin/env python
import sys
import csv
import operator
import json

#### 
# NOTE: THIS SCRIPT ASSUMES YOU'VE RUN THE FOLLOWING COMMANDS:
#
# mkdir pgs
# cp CP20_SAL.pdf pgs/CP20_SAL.pdf
# cd pgs
# pdftk CP20_SAL.pdf burst
#
####

# Make sure that you've got leading zeroes
def leading_zeroes(num):
    num = str(num)
    while len(num) < 4:
        num = "0" + num
    return num

reader = csv.reader(open("sal.csv")) # open the csv
sortedlist = sorted(reader, key=lambda t: int(t[3])) # sort the csv by page number

sal_data = []

for (i, doc) in enumerate(sortedlist):

    if i < len(sortedlist) - 1: # if we're here, that means we are not at the last document
        current, next_ = doc, sortedlist[i+1]   # get a couplet of the current and next document

        start = int(current[3].replace('"',"")) #get the current document's page number
        end = int(next_[3].replace('"',"")) #get the next document's page number
        fname = current[4].replace('"',"") + ".pdf" #get the current document's title

        j = start + 4
        page_range = []
        while j <= end + 3:
            page_range.append("pgs/pg_" + leading_zeroes(j) + ".pdf")
            j = j + 1

        import os.path
        if not os.path.isfile(fname.strip()):
            if start > end:
                print "Hey, there's a problem with: " + fname.strip()
            from subprocess import call #shell out to pdftk
            call("pdftk " + " ".join(page_range) + " cat  output tmp/" + fname.strip(), shell=True)
            print "Printing " + fname.strip() + "--" + str(start) + ":" + str(end) 

        sal_data.append({"name":fname.strip(), "title":current[0].replace('"',"").strip(), "start": str(start), "end": str(int(end) - 1), "council_period": 20})

    else:   # if we're here, we're on the last document
        start = int(doc[3].replace('"',"")) #get the current document's page number
        end = start # Go to the end
        fname = doc[4].replace('"',"") + ".pdf" #get the current document's title

        call(["pdftk pgs/pg_4778.pdf cat output tmp/" + fname.strip()], shell=True)         #shell out to pdftk
        sal_data.append({"name":fname.strip(), "title":doc[0].replace('"',"").strip(), "start": str(start), "end": end, "council_period": 20})

with open('data/metadata.json', 'w') as f:
    f.write(json.dumps(sal_data, indent=2))