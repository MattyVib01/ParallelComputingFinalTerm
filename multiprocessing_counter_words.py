import multiprocessing
import time
import os
import string
from collections import Counter
from save_csv import save_csv
from chunker import get_chunks_words
from cleaner import clean_words


def get_ngrams(seq, n):
    limite = len(seq) - n + 1
    for i in range(limite):
        yield tuple(seq[i : i+n])

# --- WORKERS ---
def process_chunk_bigrams(chunk):
    return Counter(get_ngrams(chunk, 2))

def process_chunk_trigrams(chunk):
    return Counter(get_ngrams(chunk, 3))

# --- PARALLELO ---
def compute_bigrams_parallel(word_list, num_cores):
    chunks = get_chunks_words(word_list, num_chunks=num_cores, max_ngram_size=2)
    with multiprocessing.Pool(processes=num_cores) as pool:
        partial_counters = pool.map(process_chunk_bigrams, chunks)
    return sum(partial_counters, Counter())

def compute_trigrams_parallel(word_list, num_cores):
    chunks = get_chunks_words(word_list, num_chunks=num_cores, max_ngram_size=3)
    with multiprocessing.Pool(processes=num_cores) as pool:
        partial_counters = pool.map(process_chunk_trigrams, chunks)
    return sum(partial_counters, Counter())



if __name__ == '__main__':
    percorso = os.path.join('texts', 'text8.txt')
    
    # Se vuoi usare tutti i core, usa multiprocessing.cpu_count()
    core_da_testare = 4
    print(f"--- TEST MULTIPROCESSING CON {core_da_testare} CORE ---")

    # 1. Preprocessing (fuori dal conteggio del tempo, come nel sequenziale)
    print("Fase di preprocessing...")
    with open(percorso, 'r', encoding='utf-8') as f:
        text = f.read()
    words = clean_words(text)
    
    # 2. Calcolo Bigrammi
    print("Calcolo dei Bigrammi in parallelo...")
    start_b = time.perf_counter()
    bc = compute_bigrams_parallel(words, core_da_testare)
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    # 3. Calcolo Trigrammi
    print("Calcolo dei Trigrammi in parallelo...")
    start_t = time.perf_counter()
    tc = compute_trigrams_parallel(words, core_da_testare)
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")

    # 4. Salvataggio
    save_csv(percorso, core_da_testare, "multiprocessing_words", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")
    
    # Stampa di verifica dei risultati
    print("\nTop 5 Bigrammi (Multiprocessing):", bc.most_common(5))
    print("Top 5 Trigrammi (Multiprocessing):", tc.most_common(5))