#!/usr/bin/env python
import json
import codecs
from subprocess import call
import tempfile
import os

with open('metadata.json', 'r') as fp:
    d = json.load(fp)

for m in d:
    tmp = tempfile.NamedTemporaryFile()
    # Shell out to text

    fname = 'compress/' + m["name"]
    # fname = 'compress/Act_19-584.pdf'

    out = {}
    out["title"] = m["title"]
    out["start"] = m["start"]
    out["end"] = m["end"]
    out["name"] = m["name"]
    call(['pdftotext ' + fname + ' ' + tmp.name], shell=True)
    with open(tmp.name) as f:
        out["text"] = f.read()
        
        with open('json/' + m["name"].replace('.pdf','.json'), 'w') as j:
            j.write(json.dumps(out,indent=2))
            j.close