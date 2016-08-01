#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from os import listdir
from os.path import isfile, join

import textract

if __name__ == "__main__":

    try:
        my_dir = sys.argv[1]
    except:
        my_dir = "raw_files/"

    print "Extracting text from:", my_dir

    file_list = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    
    text = {}
    for f in file_list:
        print "\tProcessing file:", f
        text[f] = textract.process( join(my_dir, f), encoding="acsii" )

    everything = { 'input': text }

    with open("corpus_data.json", "w") as file_name:
        json.dump(everything, file_name)

    print "All Done for: ", text.keys()
