import os
import csv


def save_csv(txt_filepath, metodo, tempo_bigrammi, tempo_trigrammi):
    """
    Salva i tempi in un file CSV che include il nome del metodo nel titolo.
    """
    # 1. Creiamo la cartella "results" se non esiste
    os.makedirs('results', exist_ok=True)
    
    # 2. Estraiamo il nome del file base (es. 'text1')
    nome_base = os.path.splitext(os.path.basename(txt_filepath))[0]
    
    # 3. Creiamo il percorso per il CSV INCLUDENDO il metodo
    # Es: 'results/text1_sequential_results.csv'
    csv_path = os.path.join('results', f"{nome_base}_{metodo}_results.csv")
    
    # 4. Controlliamo se il file esiste già
    file_esiste = os.path.isfile(csv_path)
    
    # 5. Apriamo il file in append
    with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Solo le due colonne dei tempi
        if not file_esiste:
            writer.writerow(['Tempo Bigrammi (s)', 'Tempo Trigrammi (s)'])
            
        # Scriviamo i tempi
        writer.writerow([f"{tempo_bigrammi:.6f}", f"{tempo_trigrammi:.6f}"])

