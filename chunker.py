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



def get_chunks_words(word_list, num_chunks, max_ngram_size):
    chunk_size = len(word_list) // num_chunks
    chunks = []
    overlap = max_ngram_size - 1
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = len(word_list) if i == num_chunks - 1 else (i + 1) * chunk_size
        
        if i < num_chunks - 1:
            end += overlap
            
        chunks.append(word_list[start:end])
    return chunks