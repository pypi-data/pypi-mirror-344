def palindrome(st):
    """
    This function checks whether the given string is a Palindrome or not.
    
    Args:
        st (str): The input string to be checked for palindrome.
        
    Returns:
        bool: True if the string is a palindrome, False otherwise.
    
    Example:
    >>> palindrome('malayalam')
    True
    """
    # Using Slicing
    if st == st[::-1]:
        return True
    else:
        return False
