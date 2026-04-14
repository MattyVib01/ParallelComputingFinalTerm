import string
import random
import time
import os
import multiprocessing
from collections import Counter
from joblib import Parallel, delayed

def clean_chars(text):
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation))

def process_chunk_char_trigrams(chunk_string):
    start_time = time.time()
    conteggio = Counter(chunk_string[i:i+3] for i in range(len(chunk_string)-2))
    elapsed_time = time.time() - start_time
    nome_processo = multiprocessing.current_process().name
    
    return conteggio, elapsed_time, len(chunk_string), nome_processo

def analizza_tempi_chunk(risultati, nome_libreria):
    large_times = []
    short_times = []
    distribution = {}     
    length = [res[2] for res in risultati]
    th = sum(length) / len(length)
    
    contatore_totale = Counter()
    
    for conteggio, tempo, lunghezza, processo in risultati:
        contatore_totale.update(conteggio)
        if lunghezza > th:
            large_times.append(tempo)
            distribution[processo] = distribution.get(processo, 0) + 1
        else:
            short_times.append(tempo)
            
    if large_times:
        print(f"Tempo medio esecuzione chunk grande: {sum(large_times)/len(large_times):.4f} sec")
        print("\nAssegnazione chunk grandi:")
        for nome_proc, conteggio_chunk in distribution.items():
            print(f"   - {nome_proc} ha elaborato {conteggio_chunk} chunk grandi")
            
    if short_times:
        print(f"\nTempo medio esecuzione chunk piccolo: {sum(short_times)/len(short_times):.6f} sec")
        
    return contatore_totale

def get_unbalanced_string_chunks(text, total_chunks=200):
    chunks = []
    eighty_percent = int(len(text) * 0.8)
    giant_chunk_size = eighty_percent // 4
    
    idx = 0
    for _ in range(4):
        chunks.append(text[idx : idx + giant_chunk_size])
        idx += giant_chunk_size
        
    remaining_chars = len(text) - idx
    tiny_chunk_size = max(1, remaining_chars // (total_chunks - 4))
    
    while idx < len(text):
        chunks.append(text[idx : idx + tiny_chunk_size])
        idx += tiny_chunk_size
        
    random.shuffle(chunks)
    return chunks

if __name__ == '__main__':
    NUM_CORES = 4  
    percorso = os.path.join('texts', 'text8.txt')
    
    print("Fase di Preprocessing")
    with open(percorso, 'r', encoding='utf-8') as f:
        text = f.read()
    cleaned_text = clean_chars(text)
    
    print("Creazione dei chunk sbilanciati")
    chunks_sbilanciati = get_unbalanced_string_chunks(cleaned_text, total_chunks=200)
    
    print("Multiprocessing:")
    start_time = time.time()
    with multiprocessing.Pool(processes=NUM_CORES) as pool:
        res_mp = pool.map(process_chunk_char_trigrams, chunks_sbilanciati)
    counter_mp = analizza_tempi_chunk(res_mp, "MULTIPROCESSING")
    mp_time = time.time() - start_time
    print(f"> Tempo Totale: {mp_time:.2f} secondi")

    print("\nJobLib:")
    start_time = time.time()
    res_jl = Parallel(n_jobs=NUM_CORES, batch_size='auto')(
        delayed(process_chunk_char_trigrams)(chunk) for chunk in chunks_sbilanciati
    )
    counter_jl = analizza_tempi_chunk(res_jl, "JOBLIB")
    jl_time = time.time() - start_time
    print(f"> Tempo Totale: {jl_time:.2f} secondi")
    
    print("\nRisultati:")
    risparmio = ((mp_time - jl_time) / mp_time) * 100
    print(f"Risparmio di tempo: {risparmio:.1f}%")