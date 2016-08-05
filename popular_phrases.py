#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import random
from os import listdir
from os.path import isfile, join, exists
from collections import Counter

from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
# Other alternatives are nltk.tokenize.punkt 
#   sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#   sent_detector.tokenize(text.strip(), realign_boundaries=False)))

import textract

class TextBucket(object):
    """ General Class for working with data structure prototyped from the MarkovBot """

    MAX_CHAIN_LEN = 1
    my_data_file = "sent_parse.json"
    my_data_dir = "sent_files/"
    stop_punctuation = "._!?"
    phrases = None # A pointer of convienance for info stores in everything['phrases']

    everything = None

    def _check_defaults(self):
        """ Helper Function to ensure internal dictionaries are setup correctly """
        try:
            self.everything['input']
        except:
            self.everything = {}
            self.everything['input'] = {}

        try:
            self.phrases = self.everything['phrases']
        except:
            self.everything['phrases'] = {}
            self.phrases = self.everything['phrases']

    def __init__(self, *args, **kwargs):
        """ Setup initial class, and ideally load data from pre-built file """
        super(TextBucket, self).__init__(*args, **kwargs)
        try:
            self.load_data()
        except:
            self._check_defaults()

    def load_data(self):
        """ Loads data (hopefully) from baseline file """
        print "Loading Data:", self.my_data_file

        with open(self.my_data_file, "r") as file_name:
            self.everything = json.loads( file_name.read() )

        ## still have to check here vs. __init__() in case file is corrupt
        self._check_defaults()

    def save_data(self):
        """ Saves data (hopefully) to baseline file """
        print "Saving Data:", self.my_data_file

        with open(self.my_data_file, "w") as file_name:
            json.dump( { 'input': self.everything['input'], 'phrases': self.phrases } , file_name)

    def add_text(self, my_dir = None):
        """ Adds all text / files from raw_file directory """
        if not my_dir:
            my_dir = self.my_data_dir
       
        ## may not have to check here but seems pragmatic
        self._check_defaults()

        print "Extracting text from:", my_dir

        file_list = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]

        for f in file_list: # Will overwrite text for any existing files
            print "\tProcessing file:", f
            self.everything['input'][f] = textract.process( join(my_dir, f), encoding="ascii" )

    def _make_chains(self, words, chain_len):
        """ Helper function to return chain pairs """

        if len(words) <= chain_len: # <= because we always want 1 stop "word" i.e. None at minimum
            words.extend( [None] * (1 + chain_len - len(words)) )

        for i in range( len(words) - chain_len ):
            yield words[i:i + chain_len + 1]

    def make_phrases(self, start = 1, end = None):
        ERRoR_TRIGGER = [u'301', u'.', None]

        if not end: end = start + 1

        for chain_len in range(start, end): # +1 because of the way range works
            self.phrases[chain_len] = []

            for f in self.everything['input']:
                for line in sent_tokenize( self.everything['input'][f] ):
                    words = word_tokenize(line)

                    for chain in self._make_chains(words, chain_len):

                        try:
                            #print "ERROR.0:", chain
                            chain = chain[:-1] # drop last item in chain as it's "value" for markov
                            chain = [c for c in chain if c is not None]
                            ## [chain.remove(None) for c in chain] # quick hack as None is breaking join
                        except: 
                            print "ERROR.1:", chain
#                           sys.exit(-1)

#                       print chain_len, " => ", chain

                        try:
                            self.phrases[chain_len].append(" ".join(chain) )
                        except:
                            print "ERROR.2:", chain
                            sys.exit(-1)

            return Counter( self.phrases[chain_len] )

    def count_phrases(self, num):
        end = num + 1
        start = 1

        self.everything['phrases'] = {}
        self.phrases = self.everything['phrases']

        for i in range(start, end):
#           try:
            self.phrases[i] = self.make_phrases(i)
            self.MAX_CHAIN_LEN = i
#           except:
#               print "FAILED"
#               pass

if __name__ == "__main__":
    bot = TextBucket()

    if not exists( bot.my_data_file ):
        bot.add_text()
        bot.save_data()

    for k in bot.everything['input'].keys():
        print "\t", k, "=> #", len(bot.everything['input'][k])
    print

#   bot.make_phrases()

    bot.count_phrases(24)
    print "Max Chain:", bot.MAX_CHAIN_LEN

#    for k in bot.phrases:
#        print "\t", k, "=>", bot.phrases[k].most_common(1)
    for i in range( bot.MAX_CHAIN_LEN, 1, -1):
        print "\t", i, "=>", bot.phrases[i].most_common(1)
