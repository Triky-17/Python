import csv
import sqlite3 
    
   
# Start permette di avere tutti i files csv completamente 
# aggiornati rispetto al database    
    
   
def start_categorie():
    """
    Carica i dati della tabella "Categorie"
    nel rispettivo csv.
    """
    categorie = open('categorie.csv', 'w+')
    categorie.close()
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Categorie')
    categorie = csv.writer(open('categorie.csv', 'w', newline = ''))
    rows = cur.fetchall()
    categorie.writerows(rows)
    conn.commit()
    conn.close()
    
          
def start_autori():
    """
    Carica i dati della tabella "Autori"
    nel rispettivo csv.
    """
    autori = open('autori.csv', 'w+')
    autori.close()
    with open('autori.csv', 'w', newline = '') as autori:
        headers = ['nome', 'cognome', 'data_nascita',
                   'luogo_nascita', 'note']
        writer = csv.DictWriter(autori, fieldnames = headers)
        writer.writeheader()
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Autori')
    autori = csv.writer(open('autori.csv', 'a', newline = ''))
    rows = cur.fetchall()
    autori.writerows(rows)
    conn.commit()
    conn.close()
        
  
def start_utenti():
    """
    Carica i dati della tabella "Utenti"
    nel rispettivo csv.
    """
    utenti = open('utenti.csv', 'w+')
    utenti.close()
    with open('utenti.csv', 'w', newline = '') as utenti:
        headers = ['tessera', 'nome', 'cognome', 'data_registrazione',
                   'telefono', 'indirizzo', 'email']
        writer = csv.DictWriter(utenti, fieldnames = headers)
        writer.writeheader()
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Utenti')
    utenti = csv.writer(open('utenti.csv', 'a', newline = ''))
    rows = cur.fetchall()
    utenti.writerows(rows)
    conn.commit()
    conn.close()
    

def start_libri():
    """
    Carica i dati della tabella "Libri"
    nel rispettivo csv.
    """
    libri = open('libri.csv', 'w+')
    libri.close()
    with open('libri.csv', 'w', newline = '') as libri:
        headers = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
                   'categorie', 'numero_copie', 'autori']
        writer = csv.DictWriter(libri, fieldnames = headers)
        writer.writeheader()
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Libri')
    libri = csv.writer(open('libri.csv', 'a', newline = ''))
    rows = cur.fetchall()
    libri.writerows(rows)
    conn.commit()
    conn.close()
    
    
def start_prestiti():
    """
    Carica i dati della tabella "Prestiti"
    nel rispettivo csv.
    """
    prestiti = open('prestiti.csv', 'w+')
    prestiti.close()
    with open('prestiti.csv', 'w', newline = '') as prestiti:
        headers = ['id_prestito', 'data_inizio', 'data_fine',
                   'isbn_libro', 'libro', 'tessera_utente', 'utente',
                   'data_consegna', 'tipo_ritardo']
        writer = csv.DictWriter(prestiti, fieldnames = headers)
        writer.writeheader()
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Prestiti')
    prestiti = csv.writer(open('prestiti.csv', 'a', newline = ''))
    rows = cur.fetchall()
    prestiti.writerows(rows)
    conn.commit()
    conn.close()    
    
    
    
def start():
    """
    Esegue tutte le funzioni di start.
    """
    start_prestiti()
    start_libri()
    start_autori()
    start_categorie()
    start_utenti()
    
    
start()
    
    

    
    
        
        