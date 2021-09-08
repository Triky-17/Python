import csv
import to_sql
import sqlite3
import datetime


def aggiungi_autore():
    """
    Permette di aggiungere un nuovo autore.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    autore = {}
    while True:
        autore['nome'] = input("Inserisci il nome dell'autore: ").title()
        if autore['nome'] == '':
            print("\nNome autore obbligatorio")
        else:
            break
    while True:
        autore['cognome'] = input("Inserisci il cognome dell'autore: ").title()
        if autore['cognome'] == '':
            print("\nCognome autore obbligatorio")
        else:
            break
    while True:
        try:
            autore['data_nascita'] = input("Inserisci data di nascita (AAAA-MM-GG): ")
            if autore['data_nascita'] == '':
                pass
            else:
                year, month, day = map(int, autore['data_nascita'].split('-'))
                autore['data_nascita'] = datetime.date(year, month, day)
            break
        except ValueError:
            print("\nData di nascita non valida")
    autore['luogo_nascita'] = input("Inserisci luogo di nascita: ").title()
    autore['note'] = input("Inserisci note (INVIO per saltare): ").capitalize()
    with open('autori.csv', 'a', newline = '') as file:
        headers = ['nome', 'cognome', 'data_nascita',
                   'luogo_nascita', 'note']
        autori = csv.DictWriter(file, fieldnames = headers)
        autori.writerow(autore)
    to_sql.sql_Autori()
    conn.commit()
    conn.close()