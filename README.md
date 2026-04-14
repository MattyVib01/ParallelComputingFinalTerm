# Conteggio di N-Grams: Analisi delle Prestazioni e Parallelizzazione

Questo progetto è un elaborato per il corso Parallel Computing per la Laurea in Ingegneria Informatica presso l'Università degli studi di Firenze.
Si concentra sull'implementazione di un algoritmo per contare le istanze di bi-gram e tri-gram all'interno di un testo. L'analisi è stata condotta considerando sia la composizione di caratteri che di parole. Lo scopo principale è lo sviluppo e il confronto di versioni parallele dell'algoritmo per ottimizzare i tempi di esecuzione su file di grandi dimensioni.

## Obiettivi del Progetto

* Creazione di un algoritmo per il conteggio di n-grams (sequenze di n caratteri o parole consecutive).
* Focalizzazione specifica su bi-gram e tri-gram (sequenze con n=2 e n=3).
* Implementazione di versioni parallele per suddividere le operazioni tra i vari core della CPU.
* Confronto tra diverse librerie di parallelizzazione in Python: Multiprocessing e JobLib.

## Implementazione e Strumenti

### Tecniche di Parallelizzazione
* **Multiprocessing**: Libreria nativa di Python che permette di aggirare il GIL (Global Interpreter Lock) creando processi figli del programma originale.
* **JobLib:** Sfrutta il backend "Loky" per gestire i cali di memoria, prevenire deadlock e condividere dati in memoria evitando clonazioni.
* **Threading:** Analizzato per valutare i limiti del context switching e della memoria condivisa in compiti CPU-bound.

### Strutture Dati e Ottimizzazione
* **Counter:** Utilizzato come Hash Map per memorizzare le istanze in modo efficiente, facilitando la somma dei contatori parziali nelle versioni parallele.
* **MapReduce:** Il task è suddiviso nelle fasi di Map (individuazione e conteggio nei chunk) e Reduce (aggregazione dei risultati intermedi).

## Dataset utilizzati

I test prestazionali sono stati effettuati su testi estratti dal Progetto Gutenberg e HuggingFace:
* Frankenstein (Mary Shelley): 78.099 parole.
* Frankenstein x50: Versione replicata 50 volte (3.904.950 parole).
* Dataset "text8": Una collezione di 100 MB di testo estratto da Wikipedia.

## Installazione e Librerie

Il progetto utilizza alcune librerie standard di Python e la libreria esterna JobLib. Per preparare l'ambiente di sviluppo, è necessario installare JobLib, con il comando sottostante:

```bash
pip install joblib

