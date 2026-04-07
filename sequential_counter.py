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

def run_analysis(execution_id):
    file_path = os.path.join('texts', 'text8.txt')

    print(f"--- Esecuzione {execution_id} ---")
    print("Fase di preprocessing...")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    chars = clean_chars(text)
    
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
    
    save_csv(file_path,1,"sequential", tempo_b, tempo_t)
    print("Tempi dell'esecuzione salvati correttamente.\n")

if __name__ == '__main__':
    # Esegui il codice 5 volte
    for i in range(0, 1):
        run_analysis(i)
    # Stampa di verifica dei risultati
    #print("\nTop 5 Bigrammi di caratteri:", bc.most_common(5)) 
    #print("Top 5 Trigrammi di caratteri:", tc.most_common(5))