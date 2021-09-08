import main
import csv
import to_sql
import sqlite3
from datetime import date
import start


def menu_utenti():
    """
    Menù utenti.
    Da qui è possibile stampare tutti gli utenti presenti
    nel database, trovare un utente o aggiungerne o cancellarne uno.
    """
    start.start()
    print('\nCosa vuoi fare?')
    choice = input('A. Visualizza Utenti\nB. Trova Utente\nC. Aggiungi Utente\nD. Cancella Utente\nE. Torna al menù precedente\n--> ').upper()
    while True:
        if choice.upper() == 'A':
            stampa_utenti()
            menu_utenti()
        if choice.upper() == 'B':
            trova_utente()
            menu_utenti()
        if choice.upper() == 'C':
            aggiungi_utente()
            menu_utenti()
        if choice.upper() == 'D':
            cancella_utente()
            menu_utenti()
        if choice.upper() == 'E':
            main.menu()
        else:
            choice = input("Inserisci un valore valido: ")


def aggiungi_utente():
    """
    Permette di aggiungere un nuovo utente.
    Dato che due utenti possono condividere sia il nome che
    il cognome, abbiamo effettuato il controllo di unicità
    su numero di telefono e email.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    utente = {}
    while True:
        utente['nome'] = input("Inserisci il nome dell'utente: ").title()
        if utente['nome'] == '':
            print("\nNome utente obbligatorio")
        else:
            break
    while True:
        utente['cognome'] = input("Inserisci il cognome dell'utente: ").title()
        if utente['cognome'] == '':
            print("\nCognome utente obbligatorio")
        else:
            break
    today = date.today()
    utente['data_registrazione'] = today.strftime("%Y-%m-%d")
    cur.execute('select telefono from Utenti')
    tel_ut = cur.fetchall()
    while True:
        try:
            while True:
                utente['telefono'] = input("Inserisci numero di telefono utente (campo obbligatorio): ")
                q = int(utente['telefono'])
                # La variabile q è stata definita per permettere di mantenere
                # un numero di telefono che inizi per 0, ma allo stesso tempo
                # per rifiutare un input che non sia totalmente numerico
                tel_check = (utente['telefono'],)
                if any(i == tel_check for i in tel_ut):
                   print("\nNumero di telefono già utilizzato")
                else:
                    break
            break
        except ValueError:
            print("\nNumero di telefono non valido")
    utente['indirizzo'] = input("Inserisci indirizzo utente: ").title()
    cur.execute('select email from Utenti')
    mail_ut = cur.fetchall()
    while True:
        utente['email'] = input("Inserisci email utente (campo obbligatorio): ")
        mail_check = (utente['email'],)
        if utente['email'] == '':
            print("\nEmail non valida")
        else:
            if any(i == mail_check for i in mail_ut):
                print("\nEmail già utilizzata")
            else:
                break
    with open('utenti.csv', 'a', newline = '') as file:
        headers = ['nome', 'cognome', 'data_registrazione',
           'telefono', 'indirizzo', 'email']
        utenti = csv.DictWriter(file, fieldnames = headers)
        utenti.writerow(utente)
    to_sql.sql_Utenti()
    conn.commit()
    conn.close()
    print("Utente aggiunto con successo")
    print('\n'.join("{}: {}".format(k, v) for k, v in utente.items()))
    return
    
       
def cancella_utente():
    """
    Permette di cancellare un utente.
    Se l'utente ha un prestito in sospeso, non sarà
    possibile cancellarlo.
    Se cancellato, anche tutti i prestiti terminati
    legati all'utente verranno rimossi.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    conn.execute("pragma foreign_keys = 1") # Rimedio a malfunzionamento foreign keys
    cur = conn.cursor()
    headers = ['tessera', 'nome', 'cognome', 'data_registrazione',
               'telefono', 'indirizzo', 'email']
    cur.execute('select tessera from Utenti')
    lista_ut = cur.fetchall()
    while True:
        try:
            tessera = int(input("Inserisci numero tessera dell'utente da cancellare: "))
            break
        except ValueError:
            print("\nNumero tessera non valido")
    check_ut = (tessera,)
    if any(x == check_ut for x in lista_ut):
        with open('utenti.csv', 'r', newline = '') as file:
            utenti = csv.DictReader(file, fieldnames = headers)
            next(utenti)
            for row in utenti:
                if int(row['tessera']) == tessera:
                    print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
        i = input("Sei sicuro di voler cancellare questo utente?:\nS: Sì\nN: No\n--> ")
        with open('prestiti.csv', 'r', newline = '') as file:
            headers_p = ['id_prestito', 'data_inizio', 'data_fine', 'isbn_libro', 'libro',
                       'tessera_utente', 'utente', 'data_consegna', 'tipo_ritardo']
            prestiti = csv.DictReader(file, fieldnames = headers_p)
            next(prestiti)
            for row in prestiti:
                if row['data_consegna'] == '' and int(row['tessera_utente']) == tessera:
                    # Se l'utente ha un libro in prestito non sarà possibile
                    # cancellarlo
                    print("L'utente ha un libro in prestito. Impossibile cancellare utente")
                    return
        while True:
            if i.upper() == 'S':
                cur.execute('delete from Utenti where tessera = ?', (tessera,))
                conn.commit()
                conn.close()
                print("Utente cancellato con successo")
                 # Verranno cancellati anche tutti i prestiti conclusi associati
                 # a questo utente
                return
            elif i.upper() == 'N':
                print("L'utente non verrà cancellato")
                return
            else:
                i = input("Inserisci un valore valido: ")
    else:
        print("Nessun utente trovato")
        return
     
        
def trova_utente():
    """
    Permette di trovare un utente nel database.
    La ricerca può essere effettuata tramite numero
    di tessera o tramite cognome.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    headers = ['tessera', 'nome', 'cognome', 'data_registrazione',
               'telefono', 'indirizzo', 'email']
    i = input("Con quale criterio vuoi effettuare la ricerca?\nT: Numero tessera\nC: Cognome\n--> ")
    while True:
        if i.upper() == 'T':
            cur.execute('select tessera from Utenti')
            lista_tessere = cur.fetchall()
            while True:
                try:
                    tessera = int(input("Inserisci tessera da cercare: "))
                    break
                except ValueError:
                    print("\nNumero tessera non valido")
            check_tessera = (tessera,)
            if any(x == check_tessera for x in lista_tessere):
                with open('utenti.csv', 'r', newline = '') as file:
                    utenti = csv.DictReader(file, fieldnames = headers)
                    next(utenti)
                    for row in utenti:
                        if int(row['tessera']) == tessera:
                            print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
                            return
            else:
                print("Nessun utente trovato")
                return
        elif i.upper() == 'C':
            cur.execute('select cognome from Utenti')
            lista_cognomi = cur.fetchall()
            cognome = input("Inserisci cognome da cercare: ").title()
            check_cognome = (cognome,)
            if any(x == check_cognome for x in lista_cognomi):
                with open('utenti.csv', 'r', newline = '') as file:
                    utenti = csv.DictReader(file, fieldnames = headers)
                    next(utenti)
                    for row in utenti:
                        if row['cognome'] == cognome:
                            print("Utente trovato:")
                            print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
                            return
            else:
                print("Nessun utente trovato")
                return
        else:
            i = input("Inserisci un valore valido: ")
        
    
def stampa_utenti():
    """
    Permette di visualizzare tutti gli utenti
    presenti nel database.
    """
    headers = ['tessera', 'nome', 'cognome', 'data_registrazione',
               'telefono', 'indirizzo', 'email']
    with open('utenti.csv', 'r', newline = '') as file:
        utenti = csv.DictReader(file, fieldnames = headers)
        next(utenti)
        for row in utenti:
            print('')
            print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
    
    