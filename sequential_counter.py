import time
import os
from collections import Counter
from cleaner import clean_chars

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
    file_path = os.path.join('texts', 'text1_large.txt')

    print("Fase di preprocessing")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    chars = clean_chars(text)
    
    print(f"Calcolo dei Bigram")
    start = time.perf_counter()
    bc=compute_bigrams(chars)
    end = time.perf_counter()
    print(f"Completato in {end - start:.4f} secondi.\n")


    print(f"Calcolo dei Trigram")
    start = time.perf_counter()
    tc=compute_trigrams(chars)
    end = time.perf_counter()
    print(f"Completato in {end - start:.4f} secondi.\n")
    
    # Stampa di verifica dei risultati
    print("Top 5 Bigrammi di caratteri:", bc.most_common(5))
    print("Top 5 Trigrammi di caratteri:", tc.most_common(5))