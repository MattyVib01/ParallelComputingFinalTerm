import time
import os
import csv
from collections import Counter
from cleaner import clean_chars, clean_words
from save_csv import save_csv

from collections import Counter

def get_ngrams(seq, n):
    limite = len(seq) - n + 1
    for i in range(limite):
        sl = seq[i : i+n]
        yield tuple(sl)

def compute_bigrams(chars):
    b_chars = Counter(get_ngrams(chars, 2))
    return b_chars

def compute_trigrams(chars):
    t_chars = Counter(get_ngrams(chars, 3))
    return t_chars

if __name__ == '__main__':
    file_path = os.path.join('texts', 'text1.txt')

    print("Fase di preprocessing...")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    chars = clean_words(text)
    
    print("Calcolo dei Bigrammi...")
    start_b = time.perf_counter()
    bc = compute_bigrams(chars)
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    print("Calcolo dei Trigrammi...")
    start_t = time.perf_counter()
    tc = compute_trigrams(chars)
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")
    
    save_csv(file_path, 1, "sequential_words", tempo_b, tempo_t)    #MODIFICA IL CSV
    print("Tempi salvati correttamente nel file csv")
    
    # Stampa di verifica dei risultati
    print("\nTop 5 Bigrammi di caratteri:", bc.most_common(5)) 
    print("Top 5 Trigrammi di caratteri:", tc.most_common(5))