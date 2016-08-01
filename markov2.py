#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from os import listdir
from os.path import isfile, join

from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
# Other alternatives are nltk.tokenize.punkt 
#   sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#   sent_detector.tokenize(text.strip(), realign_boundaries=False)))

import textract

class MarkovBot(object):
    """Markov Chain Text Generator """

    CHAIN_LENGTH = 2
    my_data_file = "corpus_data.json"
    my_data_dir = "raw_files/"
    stop_punctuation = "._!?"
    corpus = None
    everything = None

    def __init__(self, *args, **kwargs):
        super(MarkovBot, self).__init__(*args, **kwargs)
        self.load_data()

    def load_data(self):
        print "Loading Data:", self.my_data_file

        with open(self.my_data_file, "r") as file_name:
            self.everything = json.loads( file_name.read() )

        try:
            self.corpus = self.everything['corpus']
        except:
            self.corpus = {}

        try:
            self.everything['input']
        except:
            self.everything['input'] = {}

        try:
            self.CHAIN_LENGTH = everything['chain_len']
        except:
            everything['chain_len'] = self.CHAIN_LENGTH

    def save_data(self):
        print "Saving Data:", self.my_data_file

        with open("corpus_data.json", "w") as file_name:
            json.dump( { 'input': self.everything['input'], 'corpus': self.corpus } , file_name)

    def add_text(self, my_dir = None):
        if not my_dir:
            my_dir = self.my_data_dir
       
        print "Extracting text from:", my_dir

        file_list = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]

        for f in file_list: # Will overwrite text for any existing files
            print "\tProcessing file:", f
            self.everythign['input'][f] = textract.process( join(my_dir, f), encoding="acsii" )

    def _make_chains(self, words, chain_len = None):
        if not chain_len:
            chain_len = self.CHAIN_LENGTH

        if len(words) <= chain_len: # <= because we always want 1 stop "word" i.e. None at minimum
            words.extend( [None] * (1 + chain_len - len(words)) )

        for i in range( len(words) - chain_len ):
            yield words[i:i + chain_len + 1]

    def train(self, chain_len = None):
        if not chain_len:
            chain_len = self.CHAIN_LENGTH

        self.CHAIN_LEN = chain_len

        self.corpus = {}
    
        for f in self.everything['input']:
            for line in sent_tokenize( self.everything['input'][f] ):
                words = word_tokenize(line)

                for chain in self._make_chains(words):
                    k = " ".join( chain[:-1] ) # key is everything but last word
                    v = chain[-1] # value is last word
                    
                    try:
                        self.corpus[k].append(v)
                    except:
                        self.corpus[k] = [v]

    def _contains(self, text, chars):
        for c in chars:
            if c in text:
                return True
        return False

    def say_something(self, key_phrase = None, use_stops = True, max_iterations = None):
        if not key_phrase:
            key_phrase = random.choice( self.corpus.keys() )
        if not max_iterations:
            max_iterations = 50

        utterances = key_phrase.split(" ")
        chain_len = len(utterances)

        print "\nStarting with:", key_phrase
        choices = self.corpus[key_phrase]

        while choices:
            utterances.append( random.choice(choices) )

            if not utterances[-1]: # Remove if it's the stop =>  None
                utterances.pop() 
                choices = None
            elif len(utterances) > max_iterations:
                choices = None
            elif use_stops and self._contains(utterances[-1], self.stop_punctuation):
                utterances[-2] += utterances[-1] # Append ending punctuation to last word (removes space)
                utterances.pop()
                choices = None
            else:
                key_phrase = " ".join( utterances[-chain_len:] )
                choices = self.corpus[ key_phrase ]

        return " ".join(utterances)


if __name__ == "__main__":
    bot = MarkovBot()

    print bot.say_something()
