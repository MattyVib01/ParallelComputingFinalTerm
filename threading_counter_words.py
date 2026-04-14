import time
import os
import threading
import queue
from collections import Counter

from cleaner import clean_words
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

def thread_worker(target_func, chunk, result_queue):
    risultato = target_func(chunk)
    result_queue.put(risultato)

def compute_bigrams_threading_raw(chars, num_threads):
    chunks_b = get_chunks(chars, num_chunks=num_threads, max_ngram_size=2)
    
    risultati_coda = queue.Queue()
    threads = []
    
    for chunk in chunks_b:
        t = threading.Thread(
            target=thread_worker, 
            args=(process_chunk_bigrams, chunk, risultati_coda)
        )
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    partial_counters_b = []
    while not risultati_coda.empty():
        partial_counters_b.append(risultati_coda.get())
        
    return sum(partial_counters_b, Counter())

def compute_trigrams_threading_raw(chars, num_threads):
    chunks_t = get_chunks(chars, num_chunks=num_threads, max_ngram_size=3)
    
    risultati_coda = queue.Queue()
    threads = []
    
    for chunk in chunks_t:
        t = threading.Thread(
            target=thread_worker, 
            args=(process_chunk_trigrams, chunk, risultati_coda)
        )
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    partial_counters_t = []
    while not risultati_coda.empty():
        partial_counters_t.append(risultati_coda.get())
        
    return sum(partial_counters_t, Counter())


if __name__ == '__main__':
    percorso = os.path.join('texts', 'text2.txt')
    
    core_da_testare = 4
    print(f"Threading: {core_da_testare} thread")

    print("Fase di preprocessing")
    with open(percorso, 'r', encoding='utf-8') as f:
        text = f.read()
    words = clean_words(text)
    
    print("Calcolo dei Bigrammi")
    start_b = time.perf_counter()
    bc = compute_bigrams_threading_raw(words, core_da_testare)
    end_b = time.perf_counter()
    tempo_b = end_b - start_b
    print(f"Completato in {tempo_b:.4f} secondi.")

    print("Calcolo dei Trigrammi")
    start_t = time.perf_counter()
    tc = compute_trigrams_threading_raw(words, core_da_testare)
    end_t = time.perf_counter()
    tempo_t = end_t - start_t
    print(f"Completato in {tempo_t:.4f} secondi.\n")

    save_csv(percorso, core_da_testare, "threading_words", tempo_b, tempo_t)
    print("Tempi salvati correttamente nel file csv")