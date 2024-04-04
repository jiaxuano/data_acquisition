import sys

import spacy
from lxml import etree
from collections import Counter
import string
import zipfile
import os
import numpy as np
import re

"""
pytest -v

test_tfidf.py::test_gettext PASSED                                                              [ 14%]
test_tfidf.py::test_tokenize PASSED                                                             [ 28%]
test_tfidf.py::test_tokenize_2 PASSED                                                           [ 42%]
test_tfidf.py::test_doc_freq PASSED                                                             [ 57%]
test_tfidf.py::test_compute_tfidf_i PASSED                                                      [ 71%]
test_tfidf.py::test_compute_tfidf PASSED                                                        [ 85%]
test_tfidf.py::test_summarize PASSED                                                            [100%]
"""

def gettext(xmlfile) -> str:
    """
    Parse xmltext and return the text from <title> and <text> tags
    """
    root = etree.parse(xmlfile)
    title = root.xpath("./title/text()")
    ps = [i.text for i in root.xpath("./text/p")]
    output = " ".join(title+ps)
    return output

def tokenize(text, nlp) -> list:
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. 
      1. Normalize to lowercase. Strip punctuation, numbers, and `\r`, `\n`, `\t`. 
      2. Replace multiple spaces for a single space.
      3. Tokenize with spacy.
      4. Remove stopwords with spacy.
      5. Remove tokens with len <= 2.
      6. Apply lemmatization to words using spacy.
    """
    text = text.lower()
    text_clean = re.sub('[' + string.punctuation + '0-9\\r\\t\\n]', ' ', text)
    text_clean = ' '.join(text_clean.split())
    # nlp = spacy.load("/Users/ouyangjiaxuan/Downloads/DataAcq/msds692/myenv/lib/python3.10/site-packages/en_core_web_sm/en_core_web_sm-3.6.0")
    doc = nlp(text_clean)
    doc_clean = [i.lemma_ for i in doc if i.is_stop == False and len(str(i)) > 2]
    return doc_clean

def doc_freq(tok_corpus):
    """
    Returns a dictionary of the number of docs in which a word occurs.
    Input:
       tok_corpus: list of list of words
    Output:
       df: dictionary df[w] = # of docs containing w 
    """
    flat = []
    dic = dict()
    for i in tok_corpus:
        flat = flat + i
    for i in flat:
        if i not in dic:
            dic[i] = 0
    for i in dic:
        for j in tok_corpus:
            if i in j:
                dic[i] += 1
    return dic


def compute_tfidf_i(tok_doc: list, doc_freq: dict, N: int) -> dict:
    """ Returns a dictionary of tfidf for one document
        tf[w, doc] = counts[w, doc]/ len(doc)
        idf[w] = np.log(N/(doc_freq[w] + 1))
        tfidf[w, doc] = tf[w, doc]*idf[w]
    """
    ctr = Counter(tok_doc)
    tf = [ctr[i]/len(tok_doc) for i in tok_doc]
    idf = [np.log(N/(doc_freq[i]+1)) for i in tok_doc]
    tfidf_value = [tf[i]*idf[i] for i in range(len(tf))]
    tfidf_dict = {i:j for (i,j) in zip(tok_doc, tfidf_value)}
    return tfidf_dict

def compute_tfidf(tok_corpus:list, doc_freq: dict) -> dict:
    """Computes tfidf for a corpus of tokenized text.

    Input:
       tok_corpus: list of tokenized text
       doc_freq: dictionary of word to set of doc indeces
    Output:
       tfidf: list of dict 
               tfidf[i] is the dictionary of tfidf of word in doc i.
    """
    return [compute_tfidf_i(tok_corpus[i], doc_freq, len(tok_corpus)) for i in range(len(tok_corpus))]

def summarize(xmlfile, doc_freq, N,  n:int) -> list:
    """
    Given xml file, n and the tfidf dictionary 
    return up to n (word,score) pairs in a list. Discard any terms with
    scores < 0.01. Sort the (word,score) pairs by TFIDF score in reverse order.
    if words have the same score, they should be sorted in alphabet order.
    """
    text = gettext(xmlfile)
    nlp = spacy.load("en_core_web_sm")
    # The following nlp code is only for my device. My macbook cannot find en_core_web_sm unless I provide specific path
    # nlp = spacy.load("/Users/ouyangjiaxuan/Downloads/DataAcq/msds692/myenv/lib/python3.10/site-packages/en_core_web_sm/en_core_web_sm-3.6.0")
    list_words = tokenize(text,nlp)
    list_pairs = list()
    for i in range(len(list_words)):
        score = compute_tfidf_i(list_words, doc_freq, N)[list_words[i]]
        if score >= 0.01:
            pair = (list_words[i], score)
            list_pairs.append(pair)
    word_set = set()
    unsort = []
    for i in list_pairs:
        if i[0] not in word_set:
            word_set.add(i[0])
            unsort.append(i)
    sort = sorted(unsort, key=lambda x: (-x[1], x[0]), reverse = False)[:n]
    return sort