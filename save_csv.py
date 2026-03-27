import os
import csv

def save_csv(txt_filepath, num_cores, metodo, tempo_bigrammi, tempo_trigrammi):
    """
    Salva i tempi in un file CSV, includendo il numero di core utilizzati.
    """
    os.makedirs('results', exist_ok=True)
    
    nome_base = os.path.splitext(os.path.basename(txt_filepath))[0]
    csv_path = os.path.join('results', f"{nome_base}_{metodo}_results.csv")
    
    file_esiste = os.path.isfile(csv_path)
    
    with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Aggiunta la colonna 'Cores' all'inizio
        if not file_esiste:
            writer.writerow(['Cores', 'Tempo Bigrammi (s)', 'Tempo Trigrammi (s)'])
            
        writer.writerow([num_cores, f"{tempo_bigrammi:.6f}", f"{tempo_trigrammi:.6f}"])