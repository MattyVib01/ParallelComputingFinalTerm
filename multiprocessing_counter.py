import time
import os
import multiprocessing
from collections import Counter

from cleaner import clean_chars
from chunker import get_chunks
from save_csv import save_csv


# 1. Aggiorniamo get_ngrams con il generatore (yield)
def get_ngrams(seq, n):
    limite = len(seq) - n + 1
    for i in range(limite):
        fetta = seq[i : i+n]
        yield tuple(fetta)

# --- FUNZIONI WORKER (Rimangono IDENTICHE!) ---
def process_chunk_bigrams(chunk):
    # Il Counter "succhia" i dati dal generatore un elemento alla volta
    return Counter(get_ngrams(chunk, 2))

def process_chunk_trigrams(chunk):
    return Counter(get_ngrams(chunk, 3))


def compute_bigrams_parallel(chars, num_cores):
    chunks_b = get_chunks(chars, num_chunks=num_cores, max_ngram_size=2)
    with multiprocessing.Pool(processes=num_cores) as pool:
        partial_counters_b = pool.map(process_chunk_bigrams, chunks_b)
    return sum(partial_counters_b, Counter())

def compute_trigrams_parallel(chars, num_cores):
    """Suddivide il testo e calcola i trigrammi in parallelo."""
    chunks_t = get_chunks(chars, num_chunks=num_cores, max_ngram_size=3)
    with multiprocessing.Pool(processes=num_cores) as pool:
        partial_counters_t = pool.map(process_chunk_trigrams, chunks_t)
    return sum(partial_counters_t, Counter())


if __name__ == '__main__':
    percorso = os.path.join('texts', 'text1_large.txt')
    
    # Se vuoi usare tutti i core, usa multiprocessing.cpu_count()
    core_da_testare = 8
    print(f"--- TEST MULTIPROCESSING CON {core_da_testare} CORE ---")

    # 1. Preprocessing (fuori dal conteggio del tempo, come nel sequenziale)
    print("Fase di preprocessing...")
    with open(percorso, 'r', encoding='utf-8') as f:
        text = f.read()
    chars = clean_chars(text)
    
    # 2. Calcolo Bigrammi
    print("Calcolo dei Bigrammi in parallelo...")
    start_b = time.perf_counter()
    bc = compute_bigrams_parallel(chars, core_da_testare)
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    # 3. Calcolo Trigrammi
    print("Calcolo dei Trigrammi in parallelo...")
    start_t = time.perf_counter()
    tc = compute_trigrams_parallel(chars, core_da_testare)
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")

    # 4. Salvataggio
    save_csv(percorso, core_da_testare, "multiprocessing", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")
    
    # Stampa di verifica dei risultati
    # print("\nTop 5 Bigrammi (Multiprocessing):", bc.most_common(5))
    # print("Top 5 Trigrammi (Multiprocessing):", tc.most_common(5))