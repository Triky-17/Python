import csv
import sqlite3


# to_sql permette l'inserimento di dati dai csv alle rispettive
# tabelle sql


def sql_Libri():
    """
    Carica i dati da "libri.csv" nella rispettiva
    tabella in sql.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    libri = open('libri.csv', 'r')
    libri = list(csv.reader(libri, delimiter = ','))
    libri = tuple(libri[-1])
    query = ('insert or replace into Libri values (?,?,?,?,?,?,?,?)')
    cur.execute(query, libri)
    conn.commit()
    conn.close()
    
    
def sql_Categorie():
    """
    Carica i dati da "categorie.csv" nella rispettiva
    tabella in sql.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    categorie = open('categorie.csv', 'r')
    categorie = tuple(csv.reader(categorie, delimiter = ','))
    categorie = tuple(categorie[-1])
    query = ('insert or replace into Categorie values (?)')
    cur.execute(query, categorie)
    conn.commit()
    conn.close()
    
   
def sql_Autori():
    """
    Carica i dati da "autori.csv" nella rispettiva
    tabella in sql.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    autori = open('autori.csv', 'r')
    autori = tuple(csv.reader(autori, delimiter = ','))
    autori = tuple(autori[-1])
    query = ('insert or replace into Autori values (?,?,?,?,?)')
    cur.execute(query, autori)
    conn.commit()
    conn.close()
    
    
def sql_Utenti():
    """
    Carica i dati da "utenti.csv" nella rispettiva
    tabella in sql.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    utenti = open('utenti.csv', 'r')
    utenti = tuple(csv.reader(utenti, delimiter = ','))
    utenti = tuple(utenti[-1])
    query = ('insert or replace into Utenti values (null,?,?,?,?,?,?)')
    cur.execute(query, utenti)
    conn.commit()
    conn.close()
    
    
def sql_Prestiti():
    """
    Carica i dati da "prestiti.csv" nella rispettiva
    tabella in sql.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    prestiti = open('prestiti.csv', 'r')
    prestiti = list(csv.reader(prestiti, delimiter = ','))
    prestiti = tuple(prestiti[-1])
    if len(prestiti) == 8:
        # to_sql quando un prestito viene inserito per la prima volta
        # (manca id_prestito)
        query = ('insert or replace into Prestiti values (null,?,?,?,?,?,?,?,?)')
    else:
        # to_sql quando un prestito viene aggiornato con consegna o ritardo
        # (presente id_prestito)
        query = ('insert or replace into Prestiti values (?,?,?,?,?,?,?,?,?)')
    cur.execute(query, prestiti)
    conn.commit()
    conn.close()
    
    