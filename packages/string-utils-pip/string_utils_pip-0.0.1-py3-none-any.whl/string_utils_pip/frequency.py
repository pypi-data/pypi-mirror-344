def frequency(str5):
    """ This function takes string as input and returns the frequency of each character.
    
    Args:
        str5 (str): The input string.
        
    Returns:
        dict: A dictionary containing the frequency of each character.
    """
    cleaned = ''
    for char in str5:
        if char.isalnum() or char.isspace():
            cleaned += char
        else:
            cleaned += ' '  # Replace punctuation with space

    # Split into words
    words = cleaned.split()

    # Counting frequencies using a dictionary
    freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
            
    return freq