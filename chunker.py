def get_chunks(cleaned_text, num_chunks, max_ngram_size=3):
    chunk_size = len(cleaned_text) // num_chunks
    chunks = []
    overlap = max_ngram_size - 1

    for i in range(num_chunks):
        start = i * chunk_size
        if i == num_chunks - 1:
            end = len(cleaned_text)
        else:
            end = (i + 1) * chunk_size + overlap
        sl = cleaned_text[start:end]
        chunks.append(sl)
        
    return chunks