import re

def remove_whitespace(text):
    """
    Removes all whitespace from the input string.

    Args:
        text (str): Input string.

    Returns:
        str: String without any whitespace.
    """
    return ''.join(text.split())

def remove_special_characters(text):
    """
    Removes special characters from the input string, keeping only alphanumeric and spaces.

    Args:
        text (str): Input string.

    Returns:
        str: Cleaned string.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)