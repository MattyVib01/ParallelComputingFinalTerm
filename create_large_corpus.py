def create_large_corpus(file_input, file_output, moltiplicatore):
    with open(file_input, 'r', encoding='utf-8') as f:
        testo_base = f.read()

    print(f"Dimensione originale: {len(testo_base.encode('utf-8')) / (1024*1024):.2f} MB")
    print(f"Moltiplico per {moltiplicatore}...")

    with open(file_output, 'w', encoding='utf-8') as f_out:
        for _ in range(moltiplicatore):
            f_out.write(testo_base)
            f_out.write("\n") # Aggiungiamo un a capo tra un libro e l'altro

    dimensione_finale = os.path.getsize(file_output) / (1024*1024)
    print(f"File creato con successo! Nuova dimensione: {dimensione_finale:.2f} MB")

if __name__ == '__main__':
    input_path = os.path.join('texts', 'text1.txt')
    output_path = os.path.join('texts', 'text1_large.txt')
    
    # Frankenstein è circa 400KB. Moltiplicandolo per 250 otteniamo circa 100 MB.
    create_large_corpus(input_path, output_path, moltiplicatore=50)