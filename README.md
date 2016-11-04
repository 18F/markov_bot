# Initially a simple Markov-chain-based bot capable of generating statistically sayings

## Purpose

Currently an experiment in statistical text generation, the intent is to utilize this method for evaluating frequent phrases and deocding into more streamlined documentation.

## Usage

`python markov2.py`

## Data

Current Data are some sample / reference FISMA materials, a more comprehensive corpus needs to be developed and likely be a 'live download'

## Ideas

Initially there may be two “functional” thoughts, beyond just generating gibberish:

1. Long term I’d love a function for “hey, <chatbot> what does FISMA really say about <…> “ 
   Which I find most people learn by “hearsay” - that would require a lot more expertise / code than is currently present right now.

2. More immediately, I was talking w/ someone about how we could reduce “verbosity” in contract docs and think that:
   
   a. some “statistical analysis” might be helpful - e.g. sentences / word phrases that repeat as well as
   
   b. “generative analysis” - e.g. maybe if a markov bot ran many many many times with [in|de]creasing chain lengths it might be possible to determine what “key phrases” must remain but could be removed (i.e. a sentence that’s in there many times would show up more and would signify as important but also with redundancy)

## Notes:

After installing `nltk` you will likely have to use `nltk.download()` in a python REPL.
    - `book` seems to work sufficiently well for this, though might be overkill.
