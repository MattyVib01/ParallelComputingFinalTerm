import string
import os

def clean_words(text):
    """Lowercases, removes punctuation, and splits into words."""
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation)).split()

def clean_chars(text):
    """Lowercases, removes punctuation and all whitespace/newlines."""
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation + ' \n\t\r'))

