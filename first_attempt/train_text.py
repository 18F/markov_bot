#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

## PreLoading so the pickle import cost isn't paid by every item
#word_tokenizer = RegexpTokenizer("[\w']+") 
from nltk import word_tokenize


from nltk.tokenize import sent_tokenize
#item['word_list'] = tokenizer.tokenize( "".join( item['text_list'] ) )

def make_chains(words, CHAIN_LENGTH = None):
    if not CHAIN_LENGTH:
        CHAIN_LENGTH = 2
    
    # From: http://charlesleifer.com/blog/building-markov-chain-irc-bot-python-and-redis/
    # if the message is any shorter, it won't lead anywhere
    if len(words) > CHAIN_LENGTH:
        words.append(None)
    ## The above doesn't feel right to me yet
    ## I now think this is wrong - check the bot for what should be more correct, hopefully

    for i in range(len(words) - CHAIN_LENGTH):
        yield words[i:i + CHAIN_LENGTH + 1]
 
if __name__ == "__main__":

    my_data = "corpus_data.json"

    print "Loading text :", my_data

    with open(my_data, "r") as file_name:
        everything = json.loads( file_name.read() )

    everything['corpus'] = { }

    for f in everything['input']:
        for line in sent_tokenize( everything['input'][f] ):
#           words = word_tokenizer.tokenize(line)
            words = word_tokenize(line)

            for chain in make_chains(words):
                k = " ".join( chain[:-1] )
                v = chain[-1]
                try:
                    everything['corpus'][k].append(v)
                except:
                    everything['corpus'][k] = [v]

    with open("corpus_data.json", "w") as file_name:
        json.dump(everything, file_name)
