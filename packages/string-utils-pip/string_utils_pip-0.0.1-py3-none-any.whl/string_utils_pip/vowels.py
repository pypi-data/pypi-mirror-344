def extract_vowels(text):
    """
    Extract all vowels from the input string.

    Args:
        text (str): Input string.

    Returns:
        List[str]: A list of vowels found in the string.
    """
    return [char for char in text if char.lower() in 'aeiouAEIOU']