from tfidf import *
import os
import pickle

"""
1. Get a list of all xml_files in the corpus (~/data/reuters-vol1-disk1-subset).
2. Get a list of texts for all files xml_files.
3. Get a list of tokenized text (list of list of tokens).
4. Save the tokenized corpus in ~/data/tok_corpus.pickle.
"""
directory_path = sys.argv[1]

nlp = spacy.load("en_core_web_sm")
# The following nlp code is only for my device. My macbook cannot find en_core_web_sm unless I provide specific path
# nlp = spacy.load("/Users/ouyangjiaxuan/Downloads/DataAcq/msds692/myenv/lib/python3.10/site-packages/en_core_web_sm/en_core_web_sm-3.6.0")
files = os.listdir(directory_path)
list_text = [gettext(directory_path+'/'+files[i]) for i in range(len(files))]
tok_corpus = [tokenize(list_text[i],nlp) for i in range(len(list_text))]

pickle_file = os.path.expanduser("~/data/tok_corpus.pickle")
with open(pickle_file, 'wb') as file:
    pickle.dump(tok_corpus, file)
