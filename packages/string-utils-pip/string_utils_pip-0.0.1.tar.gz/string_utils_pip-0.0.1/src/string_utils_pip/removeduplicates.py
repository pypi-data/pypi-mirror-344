def removeduplicates(st):
    """Remove duplicates from string.

    Args :
    st (str) : String to remove duplicate characters.
    
    Return :
    str : String with duplicate characters removed.

    Example :
    >>> removeduplicates('hello')
    'helo'
    """
    
    new_str = ''
    for i in st:
        if i not in new_str:
            new_str += i
    return new_str