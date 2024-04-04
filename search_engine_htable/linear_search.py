# Got slate magazine data from http://www.anc.org/data/oanc/contents/
# rm'd .xml, .anc files, leaving just .txt
# 4534 files in like 55 subdirs

from words import get_text, words


def linear_search(files, terms):
    """
    Given a list of fully-qualified filenames, return a list of them
    whose file contents has all words in terms as normalized by your words() function.
    Parameter terms is a list of strings.
    Perform a linear search, looking at each file one after the other.
    """
    file_name = [f.split("/")[-1] for f in files]
    file_index = {i:j for i,j in zip(file_name, range(len(file_name)))}
    list_files = []
    for i in files:
        file_name = i.split("/")[-1]
        with open(i, 'r') as file:
            text = file.read()
        list_words = words(text)
        check_list = []
        for j in terms:
            if j in list_words:
                check_list.append(j)
        if check_list == terms:
            list_files.append(file_name)
    return list_files