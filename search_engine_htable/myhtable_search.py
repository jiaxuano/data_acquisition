# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from htable import *
from words import get_text, words


def myhtable_create_index(files):
    """
    Build an index from word to set of document indexes
    This does the exact same thing as create_index() except that it uses
    your htable.  As a number of htable buckets, use 4011.
    Returns a list-of-buckets hashtable representation.
    """
    table = htable(4011)
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
    for k in output:
        htable_put(table, k, output[k])
    return table


def myhtable_index_search(files, index, terms):
    """
    This does the exact same thing as index_search() except that it uses your htable.
    I.e., use htable_get(index, w) not index[w].
    """
    terms = [words(term)[0] for term in terms]
    file_names = [f.split("/")[-1] for f in files]
    output = []
    list_index = []
    for i in terms:
        list_index.extend(list(htable_get(index, i)))
    counts = dict()
    print(list_index)
    for j in list_index:
        if j in counts:
            counts[j] += 1
        if j not in counts:
            counts[j] = 1
    print(counts)
    for k in counts:
        if counts[k] == len(terms):
            output.append(file_names[k])
    return output