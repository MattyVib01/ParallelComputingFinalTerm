import multiprocessing
import time
import os
from collections import Counter

# I tuoi moduli personalizzati
from save_csv import save_csv
from chunker import get_chunks_words
from cleaner import clean_words

def get_ngrams(seq, n):
    limite = len(seq) - n + 1
    for i in range(limite):
        yield tuple(seq[i : i+n])

# --- WORKER CON PROFILING ---
def process_chunk_bigrams_profiled(chunk):
    # Facciamo partire il cronometro *dentro* il processo figlio
    start_time = time.perf_counter()
    counter = Counter(get_ngrams(chunk, 2))
    end_time = time.perf_counter()
    
    # Restituiamo il dizionario E il tempo effettivo di lavoro della CPU
    return counter, (end_time - start_time)


# --- PARALLELO CON PROFILING ---
def compute_bigrams_parallel_profiled(word_list, num_cores):
    chunks = get_chunks_words(word_list, num_chunks=num_cores, max_ngram_size=2)
    
    print(f"\n--- ANALISI PROFILING ({num_cores} CORE) ---")
    
    # FASE A: Mappatura e Trasporto (Misuriamo quanto tempo il processo padre aspetta)
    start_pool = time.perf_counter()
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(process_chunk_bigrams_profiled, chunks)
    end_pool = time.perf_counter()
    
    tempo_totale_pool = end_pool - start_pool
    
    # Separiamo i dizionari dai tempi registrati dai worker
    partial_counters = [res[0] for res in results]
    tempi_interni_workers = [res[1] for res in results]
    
    # FASE B: Aggregazione (Misuriamo quanto costa unire i dizionari)
    start_sum = time.perf_counter()
    final_counter = sum(partial_counters, Counter())
    end_sum = time.perf_counter()
    tempo_aggregazione = end_sum - start_sum

    # --- STAMPA DEI DATI PER LA RELAZIONE ---
    
    # Il tempo reale di CPU è dettato dal worker che ha impiegato più tempo a finire
    tempo_calcolo_puro = max(tempi_interni_workers)
    print(f"1. Tempo netto di calcolo (Max CPU):   {tempo_calcolo_puro:.4f} sec")
    
    overhead_trasporto = tempo_totale_pool - tempo_calcolo_puro
    print(f"2. Overhead di Trasporto (Pickling):   {overhead_trasporto:.4f} sec")
    
    print(f"3. Tempo di aggregazione sum():        {tempo_aggregazione:.4f} sec")
    
    tempo_totale_reale = tempo_totale_pool + tempo_aggregazione
    print(f"\nTEMPO TOTALE OPERAZIONE (1 + 4):       {tempo_totale_reale:.4f} sec")
    print("--------------------------------------\n")
    
    return final_counter, tempo_totale_reale


if __name__ == '__main__':
    percorso = os.path.join('texts', 'text2.txt')
    
    # Scegli quanti core testare
    core_da_testare = 4
    print(f"--- AVVIO SCRIPT DI BENCHMARKING SU {core_da_testare} CORE ---")

    # 1. Preprocessing (Fuori dal timer, come da prassi)
    print("Fase di preprocessing in corso (lettura e pulizia)...")
    with open(percorso, 'r', encoding='utf-8') as f:
        text = f.read()
    words = clean_words(text)
    print(f"Trovate {len(words)} parole pulite.")
    
    # 2. Calcolo Bigrammi con Profiling
    print("Avvio calcolo parallelo profilato...")
    bc, tempo_totale = compute_bigrams_parallel_profiled(words, core_da_testare)

