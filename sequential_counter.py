import time
import os
from collections import Counter
from cleaner import clean_words, clean_chars

def get_ngrams(seq, n):
    """Extracts n-grams from a sequence."""
    return [tuple(seq[i:i+n]) for i in range(len(seq) - n + 1)]

def analyze(filepath):
    """Reads file, cleans it, and returns Counters for n-grams."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Preprocessing
    words = clean_words(text)
    chars = clean_chars(text)

    # Extraction and counting
    b_words = Counter(get_ngrams(words, 2))
    t_words = Counter(get_ngrams(words, 3))

    b_chars = Counter(get_ngrams(chars, 2))
    t_chars = Counter(get_ngrams(chars, 3))

    return b_words, t_words, b_chars, t_chars

if __name__ == '__main__':
    # Usiamo os.path.join per gestire in automatico gli slash (su Windows/Mac/Linux)
    # in modo sicuro per la sottocartella "texts"
    file_path = os.path.join('texts', 'text1.txt')
    
    print(f"Starting sequential analysis of {file_path}...")
    start = time.perf_counter()
    
    # Eseguiamo l'analisi
    bw, tw, bc, tc = analyze(file_path)
    
    end = time.perf_counter()
    print(f"Done in {end - start:.4f} seconds.\n")
    
    # Stampa di verifica
    print("Top 3 Word Bigrams:", bw.most_common(3))
    print("Top 3 Word Trigrams:", tw.most_common(3))
    print("Top 3 Char Bigrams:", bc.most_common(3))
    print("Top 3 Char Trigrams:", tc.most_common(3))