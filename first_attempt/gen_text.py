#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import random
from string import punctuation

def contains(test, chars):
    for c in chars:
        if c in test:
            return True
    return False

if __name__ == "__main__":

    my_data = "corpus_data.json"
    print "Loading text :", my_data
    with open(my_data, "r") as file_name:
        everything = json.loads( file_name.read() )

    # e.g. "BY AGENCY" => "CIO"
    key_phrase = random.choice( everything['corpus'].keys() )
    utterances = key_phrase.split(" ")

    print "\nStarting with:", key_phrase
    choices = everything['corpus'][key_phrase]

    while choices:
        next_word = random.choice( choices )
        if next_word:
            utterances.append(next_word)

        if not next_word:
            choices = None
        elif len(utterances) > 500: # just want some termination
            choices = None
        elif contains(utterances[-1], "!.?_"): # typical punctuation may be stripped out in earlier proces
            utterances[-2] += utterances[-1]
            utterances.pop()
            choices = None
        else:
            key_phrase = " ".join( utterances[-2:] )
            choices = everything['corpus'][key_phrase]

    print "\t>", " ".join( utterances )
