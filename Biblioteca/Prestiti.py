import main
import csv
import to_sql
import start
import sqlite3
from datetime import date, timedelta, datetime


def menu_prestiti():
    """
    Menù prestiti.
    Da qui è possibile visualizzare tutti i prestiti
    (in corso e non), prestare o restituire un libro e
    verificare eventuali ritardi delle restituzioni.
    """
    start.start()
    print('\nCosa vuoi fare?')
    choice = input('A. Visualizza Prestiti\nB. Presta Libro\nC. Restituisci Libro\nD. Verifica Ritardi\nE. Torna al menù precedente\n--> ').upper()
    while True:
        if choice.upper() == 'A':
            visualizza_prestiti()
            menu_prestiti()
        if choice.upper() == 'B':
            presta_libro()
            menu_prestiti()
        if choice.upper() == 'C':
            restituisci_libro()
            menu_prestiti()
        if choice.upper() == 'D':
            verifica_ritardi()
            menu_prestiti()
        if choice.upper() == 'E':
            main.menu()
        else:
            choice = input("Inserisci un valore valido: ")
            
            
def presta_libro():
    """
    Permette di prestare un libro ad un utente.
    Se l'utente ha un ritardo nella riconsegna in
    corso o ha già 5 libri in prestito, non sarà
    possibile effettuare un nuovo prestito.
    Il prestito ha una durata di 30 giorni.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    prestito = {}
    headers = ['data_inizio', 'data_fine', 'isbn_libro', 'libro',
               'tessera_utente', 'utente', 'data_consegna', 'tipo_ritardo']
    prestito['data_inizio'] = date.today().strftime("%Y-%m-%d")
    prestito['data_fine'] = (date.today() + timedelta(days = 30)).strftime("%Y-%m-%d")
    cur.execute('select isbn from Libri')
    lista_isbn = cur.fetchall()
    while True:
        try:
            prestito['isbn_libro'] = int(input("Inserisci ISBN del libro da prestare: "))
            break
        except ValueError:
            print("\nISBN non valido")
    isbn_check = (prestito['isbn_libro'],)
    if not any(x == isbn_check for x in lista_isbn):
        print("\nLibro inesistente")
        return
    else:
        headers_l = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
                   'categorie', 'numero_copie', 'autori']
        with open('libri.csv', 'r', newline = '') as file:
            libri = csv.DictReader(file)
            update = []
            for row in libri:
                if int(row['isbn']) == prestito['isbn_libro']:
                    if int(row['numero_copie']) < 1:
                        # Si controlla se nel database è presente almeno
                        # una copia del libro per il prestito
                        print("Libro non disponibile per il prestito")
                        return
                    else:
                        row['numero_copie'] = int(row['numero_copie']) - 1
                        update.append(row)
                        prestito['libro'] = row['titolo']
        with open('libri.csv', 'w', newline = '') as file:
                    libri = csv.DictWriter(file, delimiter = ',', fieldnames = headers_l)
                    libri.writerow(dict((x, x) for x in headers_l))
                    libri.writerows(update)
    cur.execute('select tessera from Utenti')
    lista_ut = cur.fetchall()
    while True:
        try:
            prestito['tessera_utente'] = int(input("Inserisci numero tessera utente: "))
            break
        except ValueError:
            print("\nNumero tessera non valido")
    ut_check = (prestito['tessera_utente'],)
    if not any(x == ut_check for x in lista_ut):
        print("\nUtente inesistente")
        return
    else:
        p = 0
        with open('prestiti.csv', 'r', newline = '') as file:
            prestiti = csv.DictReader(file)
            for row in prestiti:
                if int(row['tessera_utente']) == prestito['tessera_utente'] and row['tipo_ritardo'] == "IN RITARDO":
                    # Se l'utente ha un ritardo, per lui non sarà possibile
                    # prendere il libro in prestito
                    print("L'utente ha un ritardo. Impossibile effettuare prestito")
                    return
                elif int(row['tessera_utente']) == prestito['tessera_utente']:
                    p = p + 1
            if p >= 5:
                # Se l'utente ha già 5 libri in prestito, per lui non sarà
                # possibile prendere il libro in prestito
                print("L'utente ha raggiunto il numero massimo di prestiti (5)")
                return
    with open('utenti.csv', 'r', newline = '') as file:
       utenti = csv.DictReader(file)
       for row in utenti:
           if int(row['tessera']) == prestito['tessera_utente']:
               prestito['utente'] = str(row['nome']) + " " + str(row['cognome'])
    prestito['data_consegna'] = ''
    prestito['tipo_ritardo'] = ''
    with open('prestiti.csv', 'a', newline = '') as file:
        prestiti = csv.DictWriter(file, fieldnames = headers)
        prestiti.writerow(prestito)
    to_sql.sql_Libri()
    to_sql.sql_Prestiti()
    print("\nPrestito effettuato")
    print('\n'.join("{}: {}".format(k, v) for k, v in prestito.items()))
    return
            
        
def verifica_ritardi():
    """
    Permette di visualizzare tutti i prestiti che
    presentano un ritardo nella riconsegna del libro
    (il ritardo scatta dopo i 30 giorni dalla data
    di prestito del libro).
    """
    headers = ['id_prestito', 'data_inizio', 'data_fine',
                   'isbn_libro', 'libro', 'tessera_utente', 'utente',
                   'data_consegna', 'tipo_ritardo']
    with open('prestiti.csv', 'r', newline = '') as file:
       prestiti = csv.DictReader(file)
       if any(date.today() > datetime.strptime(row['data_fine'], '%Y-%m-%d').date() 
              and row['data_consegna'] == '' for row in prestiti):
           with open('prestiti.csv', 'r', newline = '') as file:
               prestiti = csv.DictReader(file)
               rit = []
               for row in prestiti:
                   if date.today() > datetime.strptime(row['data_fine'], '%Y-%m-%d').date() and row['data_consegna'] == '':
                       # Tutti i prestiti non ancora terminati e con data di
                       # fine passata rispetto alla data attuale vengono
                       # contrassegnati "IN RITARDO"
                       row['tipo_ritardo'] = "IN RITARDO"
                       rit.append(row)
       else:
           print("Nessun ritardo")
           return
    with open('prestiti.csv', 'w', newline = '') as file:
        prestiti = csv.DictWriter(file, delimiter = ',', fieldnames = headers)
        prestiti.writerow(dict((x, x) for x in headers))
        prestiti.writerows(rit)
    to_sql.sql_Prestiti()
    with open('prestiti.csv', 'r', newline = '') as file:
       prestiti = csv.DictReader(file)
       for row in prestiti:
           if row['tipo_ritardo'] == "IN RITARDO":
               print('')
               print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
    return
           
            
def restituisci_libro():
    """
    Permette ad un utente di restituire un libro.
    Un prestito terminato verrà comunque mantenuto in
    memoria nel database.
    Se la riconsegna è avvenuta in ritardo, tale
    informazione sarà visibile nel record del prestito.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    headers = ['id_prestito', 'data_inizio', 'data_fine', 'isbn_libro', 'libro',
               'tessera_utente', 'utente', 'data_consegna', 'tipo_ritardo']
    cur.execute('select tessera from Utenti')
    lista_ut = cur.fetchall()
    while True:
        try:
            utente = int(input("Inserisci numero tessera utente: "))
            break
        except ValueError:
            print("\nNumero tessera non valido")
    ut_check = (utente,)
    if not any(x == ut_check for x in lista_ut):
        print("\nUtente inesistente")
        return
    else:
        with open('prestiti.csv', 'r', newline = '') as file:
            prestiti = csv.DictReader(file)
            check = 0
            for row in prestiti:
                if int(row['tessera_utente']) == utente:
                    check = check + 1
            if check == 0:
                print("L'utente non ha prestiti in corso")
                return
    cur.execute('select isbn_libro, libro from Prestiti where tessera_utente = ? and data_consegna = ""', (utente,))
    lista_libri = cur.fetchall()
    lib = []
    print("Libri presi in prestito dall'utente:")
    for x in lista_libri:
        y = list(x)
        lib.append(y)
        print(' - '.join(map(str, y)))
    while True:
        try:
            libro = int(input("Inserisci ISBN del libro da restituire: "))
            break
        except ValueError:
            print("\nISBN non valido")
    l = False
    for x in lib:
        if x[0] == libro:
            r = False
            with open('libri.csv', 'r', newline = '') as file:
                libri = csv.DictReader(file)
                update = []
                for row in libri:
                    if int(row['isbn']) == libro:
                        row['numero_copie'] = int(row['numero_copie']) + 1
                        update.append(row)
            with open('libri.csv', 'w', newline = '') as file:
                headers_l = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
                             'categorie', 'numero_copie', 'autori']
                libri = csv.DictWriter(file, delimiter = ',', fieldnames = headers_l)
                libri.writerow(dict((x, x) for x in headers_l))
                libri.writerows(update)
            to_sql.sql_Libri()
            with open('prestiti.csv', 'r', newline = '') as file:
                prestiti = csv.DictReader(file)
                update = []
                for row in prestiti:
                    if int(row['tessera_utente']) == utente and int(row['isbn_libro']) == libro and row['data_consegna'] == '':
                        row['data_consegna'] = date.today().strftime("%Y-%m-%d")
                        if row['data_consegna'] > row['data_fine']:
                            # Se un libro viene consegnato in ritardo rispetto
                            # alla data di fine, il prestito terminato verrà
                            # contrassegnato come "RESTITUITO IN RITARDO"
                            row['tipo_ritardo'] = "RESTITUITO IN RITARDO"
                            r = True
                        update.append(row)
            with open('prestiti.csv', 'w', newline = '') as file:
                prestiti = csv.DictWriter(file, delimiter = ',', fieldnames = headers)
                prestiti.writerow(dict((x, x) for x in headers))
                prestiti.writerows(update)
            to_sql.sql_Prestiti()
            if r == True:
                print("Libro restituito in RITARDO")
                return
            else:
                print("Libro restituito con successo")
                return
    if l == False:
        print("L'utente non ha questo libro in prestito")
        return
            
            
            
def visualizza_prestiti():
    """
    Permette di visualizzare tutti i prestiti nel
    database, sia in corso che non.
    """
    headers = ['id_prestito', 'data_inizio', 'data_fine',
                   'isbn_libro', 'libro', 'tessera_utente', 'utente',
                   'data_consegna', 'tipo_ritardo']
    with open('prestiti.csv', 'r', newline = '') as file:
        prestiti = csv.DictReader(file, fieldnames = headers)
        next(prestiti)
        for row in prestiti:
            print('')
            print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
    
                

         
    