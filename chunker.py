def get_chunks(cleaned_text, num_chunks, max_ngram_size=3):

    # Calcoliamo la grandezza base di ogni blocco
    chunk_size = len(cleaned_text) // num_chunks
    chunks = []
    
    # L'overlap necessario è n - 1
    overlap = max_ngram_size - 1

    for i in range(num_chunks):
        start = i * chunk_size
        
        # Se siamo all'ultimo blocco, prendiamo tutto fino alla fine della stringa
        if i == num_chunks - 1:
            end = len(cleaned_text)
        else:
            # Altrimenti prendiamo la grandezza del blocco + l'overlap
            end = (i + 1) * chunk_size + overlap
            
        # "Affettiamo" la stringa e la aggiungiamo alla lista
        fetta_di_testo = cleaned_text[start:end]
        chunks.append(fetta_di_testo)
        
    return chunks