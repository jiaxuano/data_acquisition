from tfidf import *
from collections import Counter
import sys


"""
Print the most common 10 words from a documents and the word count.

1. Use gettext to get the text of the xml file.
2. Tokenize the text with tokenize.
3. Compute word counts with Counter.
4. Print most common words with counts.

$ python common.py ~/data/reuters-vol1-disk1-subset/33313newsML.xml
power 14
transmission 14
new 12
say 12
generator 12
electricity 11
cost 10
zealand 9
signal 8
charge 7
"""

path = sys.argv[1]
text = gettext(path)
nlp = spacy.load("en_core_web_sm")
# The following nlp code is only for my device. My macbook cannot find en_core_web_sm unless I provide specific path
# nlp = spacy.load("/Users/ouyangjiaxuan/Downloads/DataAcq/msds692/myenv/lib/python3.10/site-packages/en_core_web_sm/en_core_web_sm-3.6.0")
# I also have to use /Users/ouyangjiaxuan/data/reuters-vol1-disk1-subset/33313newsML.xml as the xml path, otherwise etree cannot find the path starting with ~/data/reuters-vol1-disk1-subset
tokens = tokenize(text, nlp)
ctr = Counter(tokens)
common = ctr.most_common(10)
for i in common:
    print(f'''{i[0]} {i[1]}''')
