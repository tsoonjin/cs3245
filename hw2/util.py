#!/use/bin/env python3
import os
import glob
import math
from itertools import islice

from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

stemmer = PorterStemmer()   

def create_corpus(filedir):
    ''' Creates a corpus based on files that matches the regex in file directory'''
    return PlaintextCorpusReader(filedir, ".*")

def get_doc_ids(filedir):
    return sorted(os.listdir(filedir), key=lambda x: int(x))

def normalize_token(token):
    # Converts unicode string to regular string
    return str(stemmer.stem(token.lower()))

''' Input/Output '''

def list_to_string(target_list, delimiter=','):
    ''' Generates delimiter i.e ',' separated string'''
    return delimiter.join(target_list)

def write_to_file(filepath, content):
    with open(filepath, 'w') as output:
        output.write(content)

''' Skip pointers'''

def get_skiplength(posting_list):
    return int(math.floor(math.sqrt(len(posting_list))))

def get_next_pointer(index, skip_length, posting_list):
    ''' Returns -1 if exceeds length of posting_list'''
    next_index = index + skip_length
    if index % skip_length == 0 and next_index < len(posting_list):
        return next_index
    return -1

def generate_skiplist(posting_list):
    skip_length = get_skiplength(posting_list)
    return [(i, get_next_pointer(index, skip_length, posting_list)) 
        for index, i in enumerate(posting_list)]

def posting_from_skip_list(skip_list):
    return [i[0] for i in skip_list]

''' Posting list '''

def get_posting_list(index, filepath):
    '''Retrieves a posting list given a file handle'''
    with open(filepath) as postings:
        posting_list = []

        try:
            posting_list = generate_skiplist(
                next(islice(postings, index - 1, None)).rstrip('\n').rstrip('\r\n').split(','))
        except StopIteration:
            print("Encounters end of iterator")
        return posting_list
    
if __name__ == "__main__":
    pass
