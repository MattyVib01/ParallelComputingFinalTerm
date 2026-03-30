import time
import os
import csv
from collections import Counter
from cleaner import clean_chars
from save_csv import save_csv

def get_ngrams(seq, n):
    """
    Estrae n-grammi da una sequenza in modo chiaro e passo-passo.
    """
    lista_ngrammi = []
    limite = len(seq) - n + 1
    
    for i in range(limite):
        fetta = seq[i : i+n]
        ngramma_tupla = tuple(fetta)
        lista_ngrammi.append(ngramma_tupla)
    return lista_ngrammi

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
    
    save_csv(file_path, 1, "sequential", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")
    
    # Stampa di verifica dei risultati
    #print("\nTop 5 Bigrammi di caratteri:", bc.most_common(5)) 
    #print("Top 5 Trigrammi di caratteri:", tc.most_common(5))