import os
import re
import string


def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    items =  os.listdir(root)
    return [root+'/'+i for i in items if i.endswith('.txt')]

def get_text(fileName):
    f = open(fileName, encoding='latin-1')
    s = f.read()
    f.close()
    return s


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words


def results(docs, terms):
    """
    Given a list of fully-qualifed filenames, return an HTML file
    that displays the results and up to 2 lines from the file
    that have at least one of the search terms.
    Return at most 100 results.  Arg terms is a list of string terms.
    """
    # read the docs, find the line that have at least 1 word
    basics = ['<html>', '<body>', '</body>', '</html>']
    terms_str = ' '.join(terms)
    header =  '<h2>Search result for <b>' + terms_str + '</b> in ' + str(len(docs))+ ' files.</h2>\n'
    counter = 0
    block_str = ''
    for i in docs:
        counter += 1
        if counter == 101:
            break
        # It takes rootdir outside of the function
        href = "file://" + rootdir + '/' + i
        dir = rootdir+'/'+i
        p = '<p><a href=' + href + '>' + dir + '</a><br>\n'
        with open(dir, "r") as file:
            match_line = []
            for line in file:
                lower = line.lower()
                for j in terms:
                    if j in lower:
                        match_line.append(line+'<br>')
                if len(match_line) == 2:
                    break
            match_line[-1] = match_line[-1] + '<br>\n</p>'
            line_str = '\n'.join(match_line) + '\n'
        block_str += p + line_str
    main = header + block_str
    basics.insert(-2, main)
    total = '\n'.join(basics)
    return total



def filenames(docs):
    """Return just the filenames from list of fully-qualified filenames"""
    if docs is None:
        return []
    return [os.path.basename(d) for d in docs]
