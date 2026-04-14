import string
import time
import os
from save_csv import save_csv
from collections import Counter
from joblib import Parallel, delayed
from cleaner import clean_words
from chunker import get_chunks_words

def get_ngrams(seq, n):
    limite = len(seq) - n + 1
    for i in range(limite):
        yield tuple(seq[i : i+n])

def process_chunk_bigrams(chunk):
    return Counter(get_ngrams(chunk, 2))

def process_chunk_trigrams(chunk):
    return Counter(get_ngrams(chunk, 3))


def compute_bigrams_joblib(word_list, num_cores):
    chunks = get_chunks_words(word_list, num_chunks=num_cores, max_ngram_size=2)
    partial_counters = Parallel(n_jobs=num_cores, batch_size='auto')(
        delayed(process_chunk_bigrams)(chunk) for chunk in chunks
    )
    return sum(partial_counters, Counter())

def compute_trigrams_joblib(word_list, num_cores):
    chunks = get_chunks_words(word_list, num_chunks=num_cores, max_ngram_size=3)
    partial_counters = Parallel(n_jobs=num_cores, batch_size='auto')(
        delayed(process_chunk_trigrams)(chunk) for chunk in chunks
    )
    return sum(partial_counters, Counter())




if __name__ == '__main__':
    path = os.path.join('texts', 'text8.txt')
    
    cores = 4
    print(f"JobLib: {cores} core")

    print("Fase di preprocessing")
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = clean_words(text)
    

    print("Calcolo dei Bigrammi")
    start_b = time.perf_counter()
    bc = compute_bigrams_joblib(words, cores)
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    print("Calcolo dei Trigrammi")
    start_t = time.perf_counter()
    tc = compute_trigrams_joblib(words, cores)
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")

    save_csv(path, cores, "joblib_words", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")
    
    print("\nTop 5 Bigrammi:", bc.most_common(5))
    print("Top 5 Trigrammi:", tc.most_common(5))