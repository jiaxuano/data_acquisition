"""
A hashtable represented as a list of lists with open hashing.
Each bucket is a list of (key,value) tuples
"""

def htable(nbuckets):
    """Return a list of nbuckets lists"""
    buckets = [[] for i in range(nbuckets)]
    return buckets

def hashcode(o):
    """
    Return a hashcode for strings and integers; all others return None
    For integers, just return the integer value.
    For strings, perform operation h = h*31 + ord(c) for all characters in the string
    """
    if type(o) == int:
        return o
    if type(o) == str:
        h = 0
        for c in o:
            h = h*31 + ord(c)
        return h

def bucket_indexof(table, key):
    """
    You don't have to implement this, but I found it to be a handy function.
    Return the index of the element within a specific bucket; the bucket is:
    table[hashcode(key) % len(table)]. You have to linearly
    search the bucket to find the tuple containing key.
    """
    niche_len = len(table)
    index = hashcode(key) % niche_len
    for i in range(len(table[index])):
        if table[index][i][0] == key:
            return i


def htable_put(table, key, value):
    """
    Perform the equivalent of table[key] = value
    Find the appropriate bucket indicated by key and then append (key,value)
    to that bucket if the (key,value) pair doesn't exist yet in that bucket.
    If the bucket for key already has a (key,value) pair with that key,
    then replace the tuple with the new (key,value).
    Make sure that you are only adding (key,value) associations to the buckets.
    The type(value) can be anything. Could be a set, list, number, string, anything!
    """
    niche_len = len(table)
    pair = (key, value)
    index = hashcode(key) % niche_len
    status = 'add'
    for i in table[index]:
        if i[0] == key:
            status = 'remove'
            table[index].remove(i)
            table[index].append(pair)
    if status == 'add':
        table[index].append(pair)

def htable_get(table, key):
    """
    Return the equivalent of table[key].
    Find the appropriate bucket indicated by the key and look for the
    association with the key. Return the value (not the key and not
    the association!). Return None if key not found.
    """
    niche_len = len(table)
    index = hashcode(key) % niche_len
    output = [] #changed from None
    for i in table[index]:
        if i[0] == key:
            output = i[1]
    return output


def htable_buckets_str(table):
    """
    Return a string representing the various buckets of this table.
    The output looks like:
        0000->
        0001->
        0002->
        0003->parrt:99
        0004->
    where parrt:99 indicates an association of (parrt,99) in bucket 3.
    """
    list_rows = []
    for i in range(len(table)):
        str_head = f'''{i:04}->'''
        list_pairs = []
        if len(table[i]) == 0:
            row = str_head
            list_rows.append(row)
            continue
        print(table[i])
        for j in table[i]:
            pair = str(j[0]) + ":" + str(j[1])
            list_pairs.append(pair)
        str_pairs = ", ".join(list_pairs)
        row = str_head + str_pairs
        list_rows.append(row)
    output = "\n".join(list_rows) + "\n"
    return output
    


def htable_str(table):
    """
    Return what str(table) would return for a regular Python dict
    such as {parrt:99}. The order should be in bucket order and then
    insertion order within each bucket. The insertion order is
    guaranteed when you append to the buckets in htable_put().
    """
    list_pairs = []
    for i in table:
        if len(i) == 0:
            continue
        for j in i:
            pair = str(j[0]) + ':' + str(j[1])
            list_pairs.append(pair)
    output = "{" + ", ".join(list_pairs) + "}"
    return output