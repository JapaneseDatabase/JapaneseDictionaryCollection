def deleteFromDictionary(dictionary, keys):
    '''Removes entries from a dictionary.
    
    :param dictionary: the dictionary object
    :param keys: a list of key to remove from the dictionary
    '''
    print(dictionary)
    for key in keys:
        print(key)
        del dictionary[key]
