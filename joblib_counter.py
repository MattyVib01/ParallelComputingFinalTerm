import time
import os
import multiprocessing
from collections import Counter
from joblib import Parallel, delayed

from cleaner import clean_chars
from chunker import get_chunks
from save_csv import save_csv

def get_ngrams(seq, n):
    limite = len(seq) - n + 1
    for i in range(limite):
        fetta = seq[i : i+n]
        yield tuple(fetta)

def process_chunk_bigrams(chunk):
    return Counter(get_ngrams(chunk, 2))

def process_chunk_trigrams(chunk):
    return Counter(get_ngrams(chunk, 3))

# --- FUNZIONI DI CALCOLO PARALLELO (JOBLIB) ---
def compute_bigrams_joblib(chars, num_cores):
    chunks_b = get_chunks(chars, num_chunks=num_cores, max_ngram_size=2)
    
    # Aggiunto batch_size='auto' per l'ottimizzazione intelligente del carico
    partial_counters_b = Parallel(n_jobs=num_cores, batch_size='auto')(
        delayed(process_chunk_bigrams)(chunk) for chunk in chunks_b
    )
    return sum(partial_counters_b, Counter())

def compute_trigrams_joblib(chars, num_cores):
    """Suddivide il testo e calcola i trigrammi in parallelo con Joblib."""
    chunks_t = get_chunks(chars, num_chunks=num_cores, max_ngram_size=3)
    
    # Aggiunto batch_size='auto' per l'ottimizzazione intelligente del carico
    partial_counters_t = Parallel(n_jobs=num_cores, batch_size='auto')(
        delayed(process_chunk_trigrams)(chunk) for chunk in chunks_t
    )
    return sum(partial_counters_t, Counter())


if __name__ == '__main__':
    percorso = os.path.join('texts', 'text8.txt')
    
    # Imposta qui quanti core vuoi testare (es. usa multiprocessing.cpu_count() per il massimo)
    core_da_testare = 4
    print(f"--- TEST JOBLIB CON {core_da_testare} CORE ---")

    # 1. Preprocessing (fuori dal conteggio del tempo)
    print("Fase di preprocessing...")
    with open(percorso, 'r', encoding='utf-8') as f:
        text = f.read()
    chars = clean_chars(text)
    
    # 2. Calcolo Bigrammi
    print("Calcolo dei Bigrammi in parallelo (Joblib)...")
    start_b = time.perf_counter()
    bc = compute_bigrams_joblib(chars, core_da_testare)
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    # 3. Calcolo Trigrammi
    print("Calcolo dei Trigrammi in parallelo (Joblib)...")
    start_t = time.perf_counter()
    tc = compute_trigrams_joblib(chars, core_da_testare)
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")

    # 4. Salvataggio
    save_csv(percorso, core_da_testare, "joblib", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")
    
    # Stampa di verifica dei risultati
    # print("\nTop 5 Bigrammi (Joblib):", bc.most_common(5))
    # print("Top 5 Trigrammi (Joblib):", tc.most_common(5))