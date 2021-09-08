import start
import csv
import sqlite3
import to_sql


def popola_libri():
    """
    Popola la tabella "Libri" con 3 entries.
    """
    start.start_libri()
    lib_1 = {
        'isbn': 8804668288,
        'titolo': 'Sulla Strada',
        'lingua': 'Italiano',
        'editore': 'Mondadori',
        'anno': '2016',
        'categorie': 'Thriller',
        'numero_copie': 3,
        'autori': 'Jack Kerouac'}
    lib_2 = {
        'isbn': 8804707038,
        'titolo': 'Io, Robot',
        'lingua': 'Italiano',
        'editore': 'Mondadori',
        'anno': '2018',
        'categorie': 'Fantascienza',
        'numero_copie': 2,
        'autori': 'Isaac Asimov'}
    lib_3 = {
        'isbn': 8804413158,
        'titolo': 'L\'Angelo Bruciato: La Storia Di Kurt Cobain',
        'lingua': 'Italiano',
        'editore': 'Mondadori',
        'anno': '1996',
        'categorie': 'Biografia, Musica',
        'numero_copie': 3,
        'autori': 'Dave Thompson'}
    with open('libri.csv', 'a', newline = '') as file:
        headers = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
                   'categorie', 'numero_copie', 'autori']
        libri = csv.DictWriter(file, fieldnames = headers)
        libri.writerow(lib_1)
        libri.writerow(lib_2)
        libri.writerow(lib_3)
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    libri = open('libri.csv', 'r')
    next(libri)
    libri = tuple(csv.reader(libri, delimiter = ','))
    query = ('insert or replace into Libri values (?,?,?,?,?,?,?,?)')
    cur.executemany(query, libri)
    conn.commit()
    conn.close()
    
    
def popola_autori():
    """
    Popola la tabella "Autori" con 3 entries.
    """
    start.start_autori()
    aut_1 = {
        'nome': 'Isaac',
        'cognome': 'Asimov',
        'data_nascita': '1920_01-02',
        'luogo_nascita': 'Petrovici, Russia',
        'note': ''}
    aut_2 = {
        'nome': 'Jack',
        'cognome': 'Kerouac',
        'data_nascita': '1922-03-12',
        'luogo_nascita': 'Lowell, Massachusetts',
        'note': ''}
    aut_3 = {
        'nome': 'Dave',
        'cognome': 'Thompson',
        'data_nascita': '1960-01-04',
        'luogo_nascita': 'Bideford, Regno Unito',
        'note': ''}
    with open('autori.csv', 'a', newline = '') as file:
        headers = ['nome', 'cognome', 'data_nascita',
                   'luogo_nascita', 'note']
        autori = csv.DictWriter(file, fieldnames = headers)
        autori.writerow(aut_1)
        autori.writerow(aut_2)
        autori.writerow(aut_3)
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    autori = open('autori.csv', 'r')
    next(autori)
    autori = tuple(csv.reader(autori, delimiter = ','))
    query = ('insert or replace into Autori values (?,?,?,?,?)')
    cur.executemany(query, autori)
    conn.commit()
    conn.close()
    
    
def popola_categorie():
    """
    Popola la tabella "Categorie" con 11 entries
    """
    start.start_categorie()
    Categorie = ["Diritto", "Informatica", "Politica", "Avventura",
                  "Giallo", "Fantascienza", "Economia", "Horror", "Thriller",
                  "Biografia", "Musica"]
    for y in Categorie:
        x = []
        x.append(y)
        with open('categorie.csv', 'a', newline = '') as file:
            categorie = csv.writer(file)
            categorie.writerow(x)
        to_sql.sql_Categorie()
        
        
def popola_utenti():
    """
    Popola la tabella "Utenti" con 3 entries.
    """
    start.start_utenti()
    ut_1 = {
        'nome': 'Ugo',
        'cognome': 'Fantozzi',
        'data_registrazione': '2021-03-27',
        'telefono': 3428765645,
        'indirizzo': 'Roma, Via Giovanni Battista Bodoni 79',
        'email': 'ugo.fantozzi@gmail.com'}
    ut_2 = {
        'nome': 'Piero',
        'cognome': 'Scotti',
        'data_registrazione': '2021-02-21',
        'telefono': 3489991717,
        'indirizzo': 'Miradolo, Via Franco 17',
        'email': 'pierscott@hotmail.com'}
    ut_3 = {
        'nome': 'Guida',
        'cognome': 'Lavespa',
        'data_registrazione': '2021-04-01',
        'telefono': 3474511910,
        'indirizzo': 'Milano, Via Piaggio 90',
        'email': 'guida.50special@tiscali.com'}
    with open('utenti.csv', 'a', newline = '') as file:
        headers = ['nome', 'cognome', 'data_registrazione',
                   'telefono', 'indirizzo', 'email']
        utenti = csv.DictWriter(file, fieldnames = headers)
        utenti.writerow(ut_1)
        utenti.writerow(ut_2)
        utenti.writerow(ut_3)
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    utenti = open('utenti.csv', 'r')
    next(utenti)
    utenti = tuple(csv.reader(utenti, delimiter = ','))
    query = ('insert or replace into Utenti values (null,?,?,?,?,?,?)')
    cur.executemany(query, utenti)
    conn.commit()
    conn.close()
    
  
def popola_prestiti():
    """
    Popola la tabella "Prestiti" con 3 entries.
    """
    start.start_prestiti()
    pre_1 = {
        'data_inizio': '2021-02-26',
        'data_fine': '2021-03-28',
        'isbn_libro': 8804707038,
        'libro': 'Io, Robot',
        'tessera_utente': 2,
        'utente': 'Piero Scotti',
        'data_consegna': '2021-03-27',
        'tipo_ritardo': ''}
    pre_2 = {
        'data_inizio': '2021-04-02',
        'data_fine': '2021-05-02',
        'isbn_libro': 8804668288,
        'libro': 'Sulla Strada',
        'tessera_utente': 1,
        'utente': 'Ugo Fantozzi',
        'data_consegna': '2021-05-07',
        'tipo_ritardo': 'RESTITUITO IN RITARDO'}
    pre_3 = {
        'data_inizio': '2021-04-07',
        'data_fine': '2021-05-07',
        'isbn_libro': 8804413158,
        'libro': 'L\'Angelo Bruciato: La Storia Di Kurt Cobain',
        'tessera_utente': 3,
        'utente': 'Guida Lavespa',
        'data_consegna': '',
        'tipo_ritardo': 'IN RITARDO'}
    with open('prestiti.csv', 'a', newline = '') as file:
        headers = ['data_inizio', 'data_fine', 'isbn_libro',
                   'libro', 'tessera_utente', 'utente', 'data_consegna',
                   'tipo_ritardo']
        prestiti = csv.DictWriter(file, fieldnames = headers)
        prestiti.writerow(pre_1)
        prestiti.writerow(pre_2)
        prestiti.writerow(pre_3)
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    prestiti = open('prestiti.csv', 'r')
    next(prestiti)
    prestiti = tuple(csv.reader(prestiti, delimiter = ','))
    query = ('insert or replace into Prestiti values (null,?,?,?,?,?,?,?,?)')
    cur.executemany(query, prestiti)
    conn.commit()
    conn.close()
  
    
    
def popola():
    """
    Esegue tutte le funzioni di popolamento.
    """
    popola_libri()
    popola_autori()
    popola_categorie()
    popola_utenti()
    popola_prestiti()
    
popola()
start.start()   
    
    
