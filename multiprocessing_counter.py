import time
import os
import multiprocessing
from collections import Counter

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
    path = os.path.join('texts', 'text2.txt')
    cores = 8
    print(f"Multiprocessing: {cores} core")

    print("Fase di preprocessing")
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    chars = clean_chars(text)
    
    print("Calcolo dei Bigrammi")
    start_b = time.perf_counter()
    bc = compute_bigrams_parallel(chars, cores)
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    print("Calcolo dei Trigrammi")
    start_t = time.perf_counter()
    tc = compute_trigrams_parallel(chars, cores)
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")

    save_csv(path, cores, "multiprocessing", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")
    
    # print("\nTop 5 Bigrammi (Multiprocessing):", bc.most_common(5))
    # print("Top 5 Trigrammi (Multiprocessing):", tc.most_common(5))