import main
import csv
import to_sql
import sqlite3
import start
import datetime


def menu_libri():
    """
    Menù libri.
    Da qui è possibile visualizzare l'intero catalogo
    dei libri presenti nel database, trovare un libro,
    aggiungerne, aggiornarne o cancellarne uno.
    """
    start.start()
    print('\nCosa vuoi fare?')
    choice = input('A. Catalogo Libri\nB. Trova Libro\nC. Aggiungi Libro\nD. Aggiorna Libro\nE. Cancella Libro\nF. Torna al menù precedente\n--> ').upper()
    while True:
        if choice.upper() == 'A':
            stampa_catalogo()
            menu_libri()
        if choice.upper() == 'B':
            trova_libro()
            menu_libri()
        if choice.upper() == 'C':
            aggiungi_libro()
            menu_libri()
        if choice.upper() == 'D':
            aggiorna_libro()
            menu_libri()
        if choice.upper() == 'E':
            cancella_libro()
            menu_libri()
        if choice.upper() == 'F':
            main.menu()
        else:
            choice = input("Inserisci un valore valido: ")


def aggiungi_libro():
    """
    Permette di aggiungere un nuovo libro.
    Se il libro esiste già (ISBN univoco), sarà 
    possibile aggiungere altre copie a quelle già
    presenti nel database.
    Da questa funzione è possibile aggiungere anche
    nuove categorie o autori se non presenti nel database
    al momento dell'inserimento del libro.'
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    libro = {}
    headers = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
               'categorie', 'numero_copie', 'autori']
    cur.execute('select isbn from Libri')
    lista_isbn = cur.fetchall()
    while True:
        try:
            libro['isbn'] = int(input("Inserisci ISBN (campo obbligatorio): "))
            break
        except ValueError:
            print("\nISBN non valido")
    isbn_check = (libro['isbn'],)
    if any(x == isbn_check for x in lista_isbn):
        # Se il libro già esiste, sarà possibile aggiungere delle copie
        i = input("Libro già esistente, vuoi aggiungere delle copie?\nS: Sì\nN: No\n--> ")
        while True:
            if i.upper() == 'S':
                while True:
                    try:
                        c = int(input("Inserisci numero copie: "))
                        if c >= 0:
                            break
                        else:
                            print("\nValore non valido")
                    except ValueError:
                        print("\nValore non valido")
                with open('libri.csv', 'r', newline = '') as file:
                    libri = csv.DictReader(file)
                    update = []
                    for row in libri:
                        if int(row['isbn']) == libro['isbn']:
                            row['numero_copie'] = int(row['numero_copie']) + c
                            update.append(row)
                with open('libri.csv', 'w', newline = '') as file:
                    libri = csv.DictWriter(file, delimiter = ',', fieldnames = headers)
                    libri.writerow(dict((x, x) for x in headers))
                    libri.writerows(update)
                to_sql.sql_Libri()
                print("Copie aggiunte con successo")
                return
            elif i.upper() == 'N':
                print("Non verranno aggiunte copie")
                return
            else:
                i = input("Inserisci un valore valido: ")
    else:
        libro['titolo'] = input("Inserisci titolo: ").title()
        libro['lingua'] = input("Inserisci lingua: ").title()
        libro['editore'] = input("Inserisci editore: ").title()
        while True:
            try:
                libro['anno'] = input("Inserisci anno (edizione): ")
                if libro['anno'] == '':
                    pass
                else:
                    libro['anno'] = int(libro['anno'])
                break
            except ValueError:
                print("\nValore non valido")
        while True:
            try:
                i = input("Quante categorie vuoi inserire? (Nessun input = 0): ")
                if i == '':
                    i = 0
                else:
                    i = int(i)
                break
            except ValueError:
                print("\nValore non valido")
        cat = []
        cur.execute('select * from Categorie')
        lista_cat = cur.fetchall()
        while i > 0:
            c = ''
            x = input("Inserisci una categoria: ").title()
            check_cat = (x,)
            if check_cat not in lista_cat:
               # Se la categoria inserita non esiste sarà possibile aggiungerla
               # al database
               c = input("La categoria non esiste, vuoi aggiungerla?\nS: Sì\nN: No\n--> ")
               while True:
                   if c.upper() == 'S':
                       conn = sqlite3.connect('biblioteca.sqlite')
                       agg = []
                       agg.append(x)
                       with open('categorie.csv', 'a', newline = '') as file:
                           categorie = csv.writer(file)
                           categorie.writerow(agg)
                       to_sql.sql_Categorie()
                       print("Categoria aggiunta con successo")
                       conn.commit()
                       conn.close()
                       break
                   elif c.upper() == 'N':
                       print("Il libro non può avere una categoria inesistente")
                       break
                   else:
                       c = input("Inserisci un valore valido: ")
            if c.upper() != 'N':
                if x in cat:
                    print("\nIl libro ha già questa categoria")
                else:
                    cat.append(x)
                    i = i - 1 
        cat = ', '.join(map(str, cat))
        libro['categorie'] = cat
        while True:
            try:
                libro['numero_copie'] = int(input("Inserisci numero copie (campo obbligatorio): "))
                if libro['numero_copie'] >= 0:
                    break
                else:
                    print("\nValore non valido")
            except ValueError:
                print("\nValore non valido")
        while True:
            try:
                i = input("Quanti autori vuoi inserire? (Nessun input = 0): ")
                if i == '':
                    i = 0
                else:
                    i = int(i)
                break
            except ValueError:
                print("\nValore non valido")
        aut = []
        cur.execute('select nome, cognome from Autori')
        lista_aut = cur.fetchall()
        while i > 0:
            c = ''
            print("\nInserisci autore:")
            nome = input("Inserisci nome autore: ").title()
            cognome = input("Inserisci cognome autore: ").title()
            x = (nome, cognome)
            if x not in lista_aut:
                # Se l'autore inserito non esiste sarà possibile aggiungerlo
                # al database
                c = input("L'autore non esiste, vuoi aggiungerlo?\nS: Sì\nN: No\n--> ")
                while True:
                   if c.upper() == 'S':
                       conn = sqlite3.connect('biblioteca.sqlite')
                       autore = {}
                       autore['nome'] = nome
                       autore['cognome'] = cognome
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
                            headers_aut = ['nome', 'cognome', 'data_nascita',
                                       'luogo_nascita', 'note']
                            autori = csv.DictWriter(file, fieldnames = headers_aut)
                            autori.writerow(autore)
                       to_sql.sql_Autori()
                       print("Autore aggiunto con successo")
                       print('')
                       conn.commit()
                       conn.close()
                       break 
                   elif c.upper() == 'N':
                       print("Il libro non può avere un autore inesistente")
                       break
                   else:
                       c = input("Inserisci un valore valido: ")
            if c.upper() != 'N':
                x = ' '.join(x)
                if x in aut:
                    print("\nIl libro ha già questo autore")
                else:
                    aut.append(x)
                    i = i - 1
        aut = ', '.join(map(str, aut))
        libro['autori'] = aut
        with open('libri.csv', 'a', newline = '') as file:
            libri = csv.DictWriter(file, fieldnames = headers)
            libri.writerow(libro)
        to_sql.sql_Libri()
        print("Libro aggiunto con successo")
        print('\n'.join("{}: {}".format(k, v) for k, v in libro.items()))
        return
        
        
def aggiorna_libro():
    """
    Permette di aggiornare le informazioni di un libro.
    Le informazioni che è possibile aggiornare sono
    titolo, editore e numero di copie.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    headers = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
               'categorie', 'numero_copie', 'autori']
    cur.execute('select isbn from Libri')
    lista_isbn = cur.fetchall()
    while True:
        try:
            isbn = int(input("Inserisci ISBN del libro da aggiornare: "))
            break
        except ValueError:
            print("\nISBN non valido")
    check_isbn = (isbn,)
    if any(x == check_isbn for x in lista_isbn):
        i = input("Quale campo vuoi aggiornare?:\nT: Titolo\nE: Editore\nC: Numero copie\n--> ")
        while True:
            if i.upper() == 'T':
                with open('libri.csv', 'r', newline = '') as file:
                        libri = csv.DictReader(file)
                        update = []
                        title = input("Inserisci nuovo titolo: ").title()
                        for row in libri:
                            if int(row['isbn']) == isbn:
                                row['titolo'] = title
                                update.append(row)
                                print("Titolo aggiornato con successo")
                        break
            if i.upper() == 'E':
                with open('libri.csv', 'r', newline = '') as file:
                        libri = csv.DictReader(file)
                        update = []
                        editore = input("Inserisci nuovo editore: ").title()
                        for row in libri:
                            if int(row['isbn']) == isbn:
                                row['editore'] = editore
                                update.append(row)
                                print("Editore aggiornato con successo")
                        break
            if i.upper() == 'C':
                with open('libri.csv', 'r', newline = '') as file:
                        libri = csv.DictReader(file)
                        update = []
                        while True:
                            try:
                                copie = int(input("Inserisci nuovo numero di copie: "))
                                break
                            except ValueError:
                                print("\nValore non valido")
                        for row in libri:
                            if int(row['isbn']) == isbn:
                                row['numero_copie'] = copie
                                update.append(row)
                                print("Numero copie aggiornato con successo")
                        break
            else:
                i = input("Inserisci un valore valido: ")
        with open('libri.csv', 'w', newline = '') as file:
                    libri = csv.DictWriter(file, delimiter = ',', fieldnames = headers)
                    libri.writerow(dict((x, x) for x in headers))
                    libri.writerows(update)
        to_sql.sql_Libri()
        return
    else:
        print("Il libro non esiste")
        
        
def cancella_libro():
    """
    Permette di cancellare un libro.
    Se il libro è in prestito, non sarà possibile
    cancellarlo.
    Quando rimosso, anche tutti i prestiti conclusi
    del libro verranno cancellati.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    conn.execute("pragma foreign_keys = 1") # Rimedio a malfunzionamento foreign keys
    cur = conn.cursor()
    headers = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
               'categorie', 'numero_copie', 'autori']
    cur.execute('select isbn from Libri')
    lista_isbn = cur.fetchall()
    while True:
        try:
            isbn = int(input("Inserisci ISBN del libro da cancellare: "))
            break
        except ValueError:
            print("\nISBN non valido")
    check_isbn = (isbn,)
    if any(x == check_isbn for x in lista_isbn):
        with open('libri.csv', 'r', newline = '') as file:
            libri = csv.DictReader(file, fieldnames = headers)
            next(libri)
            for row in libri:
                if int(row['isbn']) == isbn:
                    print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
        i = input("Sei sicuro di voler cancellare questo libro?:\nS: Sì\nN: No\n--> ")
        with open('prestiti.csv', 'r', newline = '') as file:
            headers_p = ['id_prestito', 'data_inizio', 'data_fine', 'isbn_libro', 'libro',
                       'tessera_utente', 'utente', 'data_consegna', 'tipo_ritardo']
            prestiti = csv.DictReader(file, fieldnames = headers_p)
            next(prestiti)
            for row in prestiti:
                if row['data_consegna'] == '' and int(row['isbn_libro']) == isbn:
                    # Se il libro è in prestito non sarà possibile cancellarlo
                    print("Libro attualmente in prestito. Impossibile cancellare libro")
                    return
        while True:
            if i.upper() == 'S':
                cur.execute('delete from Libri where isbn = ?', (isbn,))
                conn.commit()
                conn.close()
                print("Libro cancellato con successo")
                # Verranno cancellati anche tutti i prestiti conclusi associati
                # a questo libro
                return
            elif i.upper() == 'N':
                print("Il libro non verrà cancellato")
                return
            else:
                i = input("Inserisci un valore valido: ")
    else:
        print("Nessun libro trovato")
        return
        
               
def trova_libro():
    """
    Permette di trovare un libro nella biblioteca.
    La ricerca può essere effettuata tramite ISBN 
    o titolo.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    headers = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
                   'categorie', 'numero_copie', 'autori']
    i = input("Con quale criterio vuoi effettuare la ricerca?\nI: ISBN\nT: Titolo\n--> ")
    while True:
        if i.upper() == 'I':
            cur.execute('select isbn from Libri')
            lista_isbn = cur.fetchall()
            while True:
                try:
                    isbn = int(input("Inserisci ISBN da cercare: "))
                    break
                except ValueError:
                    print("\nISBN non valido")
            check_isbn = (isbn,)
            if any(x == check_isbn for x in lista_isbn):
                with open('libri.csv', 'r', newline = '') as file:
                    libri = csv.DictReader(file, fieldnames = headers)
                    next(libri)
                    for row in libri:
                        if int(row['isbn']) == isbn:
                            print("\nLibro trovato:")
                            print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
                            return
            else:
                print("Nessun libro trovato")
                return
        elif i.upper() == 'T':
            cur.execute('select titolo from Libri')
            lista_titoli = cur.fetchall()
            titolo = input("Inserisci titolo da cercare: ").title()
            check_titolo = (titolo,)
            if any(x == check_titolo for x in lista_titoli):
                with open('libri.csv', 'r', newline = '') as file:
                    libri = csv.DictReader(file, fieldnames = headers)
                    next(libri)
                    for row in libri:
                        if row['titolo'] == titolo:
                            print("Libro trovato:")
                            print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
                            return
            else:
                print("Nessun libro trovato")
                return
        else:
            i = input("Inserisci un valore valido: ")
        
        
def stampa_catalogo():
    """
    Permette di visualizzare il catalogo con tutti
    i libri presenti nella biblioteca.
    """
    headers = ['isbn', 'titolo', 'lingua', 'editore', 'anno',
               'categorie', 'numero_copie', 'autori']
    with open('libri.csv', 'r', newline = '') as file:
        libri = csv.DictReader(file, fieldnames = headers)
        next(libri)
        for row in libri:
            print('')
            print('\n'.join("{}: {}".format(k, v) for k, v in row.items()))
            
    
                
                
                