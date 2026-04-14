import multiprocessing
import time
import os
from collections import Counter
from save_csv import save_csv
from chunker import get_chunks_words
from cleaner import clean_words

def get_ngrams(seq, n):
    limite = len(seq) - n + 1
    for i in range(limite):
        yield tuple(seq[i : i+n])

def process_chunk_bigrams_profiled(chunk):
    start_time = time.perf_counter()
    counter = Counter(get_ngrams(chunk, 2))
    end_time = time.perf_counter()
    
    return counter, (end_time - start_time)


def compute_bigrams_parallel_profiled(word_list, num_cores):
    chunks = get_chunks_words(word_list, num_chunks=num_cores, max_ngram_size=2)
    
    print(f"\nProfiling: ({num_cores} core")
    
    start_pool = time.perf_counter()
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(process_chunk_bigrams_profiled, chunks)
    end_pool = time.perf_counter()
    
    tempo_totale_pool = end_pool - start_pool
    
    partial_counters = [res[0] for res in results]
    tempi_interni_workers = [res[1] for res in results]
    
    start_sum = time.perf_counter()
    final_counter = sum(partial_counters, Counter())
    end_sum = time.perf_counter()
    tempo_aggregazione = end_sum - start_sum

    tempo_calcolo_puro = max(tempi_interni_workers)
    print(f"Tempo netto di calcolo (Max CPU):   {tempo_calcolo_puro:.4f} sec")
    
    overhead_trasporto = tempo_totale_pool - tempo_calcolo_puro
    print(f"Overhead di Trasporto (Pickling):   {overhead_trasporto:.4f} sec")
    
    print(f"Tempo di aggregazione sum():        {tempo_aggregazione:.4f} sec")
    
    tempo_totale_reale = tempo_totale_pool + tempo_aggregazione
    print(f"\nTempo totale:       {tempo_totale_reale:.4f} sec")
    
    return final_counter, tempo_totale_reale


if __name__ == '__main__':
    path = os.path.join('texts', 'text2.txt')
    
    core_da_testare = 4
    print(f"Avvio script: {core_da_testare} core")

    print("Fase di preprocessing")
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = clean_words(text)
    print(f"Trovate {len(words)} parole.")
    
    print("Avvio calcolo parallelo profilato")
    bc, tempo_totale = compute_bigrams_parallel_profiled(words, core_da_testare)

