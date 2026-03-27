import time
import os
import multiprocessing
from collections import Counter

from cleaner import clean_chars
from chunker import get_chunks
from save_csv import save_csv

def get_ngrams(seq, n):
    lista_ngrammi = []
    limite = len(seq) - n + 1
    for i in range(limite):
        fetta = seq[i : i+n]
        lista_ngrammi.append(tuple(fetta))
    return lista_ngrammi

def process_chunk_bigrams(chunk):
    return Counter(get_ngrams(chunk, 2))

def process_chunk_trigrams(chunk):
    return Counter(get_ngrams(chunk, 3))

def multiprocessing_counter(file_path, num_cores=None):

    # Se l'utente non specifica i core, prendiamo il massimo disponibile
    if num_cores is None:
        num_cores = multiprocessing.cpu_count()
        
    print(f"Fase di preprocessing per {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    chars = clean_chars(text)
    
    print(f"Avvio suddivisione del testo per {num_cores} core...")
    
    # Dividiamo il testo esattamente nel numero di core richiesti
    chunks_b = get_chunks(chars, num_chunks=num_cores, max_ngram_size=2)
    chunks_t = get_chunks(chars, num_chunks=num_cores, max_ngram_size=3)

    print("Calcolo dei Bigram in parallelo...")
    start_b = time.perf_counter()
    with multiprocessing.Pool(processes=num_cores) as pool:
        partial_counters_b = pool.map(process_chunk_bigrams, chunks_b)
    bc = sum(partial_counters_b, Counter())
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    print("Calcolo dei Trigram in parallelo...")
    start_t = time.perf_counter()
    with multiprocessing.Pool(processes=num_cores) as pool:
        partial_counters_t = pool.map(process_chunk_trigrams, chunks_t)
    tc = sum(partial_counters_t, Counter())
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")

    # Salvataggio nel CSV passando il numero di core esatto
    save_csv(file_path, num_cores, "multiprocessing", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")

    return bc, tc

if __name__ == '__main__':
    percorso = os.path.join('texts', 'text1_large.txt')
    

    core_da_testare = 8
    print(f"Usati {core_da_testare} core")
    risultato_bc, risultato_tc = multiprocessing_counter(percorso, num_cores=core_da_testare)
    
    # Stampa di verifica dei risultati
    #print("\nTop 5 Bigrammi (Multiprocessing):", risultato_bc.most_common(5))
    #print("Top 5 Trigrammi (Multiprocessing):", risultato_tc.most_common(5))