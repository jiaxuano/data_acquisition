from collections import defaultdict  # https://docs.python.org/2/library/collections.html

from words import get_text, words


def create_index(files):
    """
    Given a list of fully-qualified filenames, build an index from word
    to set of document IDs. A document ID is just the index into the
    files parameter (indexed from 0) to get the file name. Make sure that
    you are mapping a word to a set of doc IDs, not a list.
    For each word w in file i, add i to the set of document IDs containing w
    Return a dict object mapping a word to a set of doc IDs.
    """
    file_name = [f.split("/")[-1] for f in files]
    file_index = {i:j for i,j in zip(file_name, range(len(file_name)))}
    output = dict()
    for i in files:
        file_name = i.split("/")[-1]
        with open(i, 'r') as file:
            text = file.read()
            set_words = set(words(text))
            set_words = sorted(set_words)
            for j in set_words:
                if j not in output:
                    output[j] = {file_index[file_name]}
                if j in output:
                    output[j].add(file_index[file_name])
    return output
        


def index_search(files, index, terms):
    """
    Given an index and a list of fully-qualified filenames, return a list of
    filenames whose file contents has all words in terms parameter as normalized
    by your words() function.  Parameter terms is a list of strings.
    You can only use the index to find matching files; you cannot open the files
    and look inside.
    """
    terms = [words(term)[0] for term in terms]
    file_names = [f.split("/")[-1] for f in files]
    output = []
    list_index = []
    if all(term in index for term in terms):
        for i in terms:
            list_index.extend(list(index[i]))
        counts = dict()
        print(list_index)
        for j in list_index:
            if j in counts:
                counts[j] += 1
            if j not in counts:
                counts[j] = 1
        print('ahoy there!')
        print(counts)
        for k in counts:
            if counts[k] == len(terms):
                output.append(file_names[k])
    return output