import main
import csv
import to_sql
import sqlite3
import start


def menu_categorie():
    """
    Menù categorie.
    Da qui è possibile stampare tutte le categorie presenti
    nel database o aggiungere o cancellare una categoria.
    """
    start.start()
    print('\nCosa vuoi fare?')
    choice = input('A. Visualizza Categorie\nB. Aggiungi Categoria\nC. Cancella Categoria\nD. Torna al menù precedente\n--> ').upper()
    while True:
        if choice.upper() == 'A':
            stampa_categorie()
            menu_categorie()
        if choice.upper() == 'B':
            aggiungi_categoria()
            menu_categorie()
        if choice.upper() == 'C':
            cancella_categoria()
            menu_categorie()
        if choice.upper() == 'D':
            main.menu()
        else:
            choice = input("Inserisci un valore valido: ")


def aggiungi_categoria():
    """
    Permette di aggiungere una nuova categoria.
    Se la categoria inserita è già esistente, allora
    non verrà aggiunta.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Categorie')
    lista_cat = cur.fetchall()
    while True:
        x = []
        categoria = input("Inserisci categoria da aggiungere: ").title()
        x.append(categoria)
        check_cat = (categoria,)
        if check_cat in lista_cat:
            print("\nCategoria già esistente")
        else:
            break
    with open('categorie.csv', 'a', newline = '') as file:
        categorie = csv.writer(file)
        categorie.writerow(x)
    to_sql.sql_Categorie()
    print("\nCategoria aggiunta con successo")
    conn.commit()
    conn.close()
    return
    
    
def cancella_categoria():
    """
    Permette di cancellare una categoria esistente.
    La categoria cancellata verrà rimossa anche da tutti i
    libri della biblioteca che la contengono.
    """
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Categorie')
    lista_cat = cur.fetchall()
    stampa_categorie()
    cat = input("Quale categoria vuoi cancellare?: ").title()
    check_cat = (cat,)
    if any(x == check_cat for x in lista_cat):
        cur.execute('delete from Categorie where categoria = ?', (cat,))
        cur.execute('select categorie from Libri')
        cat_libri = cur.fetchall()
        cat_remove = []
        for x in cat_libri:
            for y in x:
                y = y.split(', ')
                cat_remove.append(y)
        for x in cat_remove:
            if cat in x:
                old_x = x
                old_x = ', '.join(map(str, old_x))
                x.remove(cat)
                x = ', '.join(map(str, x))
                cur.execute('update Libri set categorie = ? where categorie = ?', [x, old_x])
        conn.commit()
        conn.close()
        print("Categoria cancellata con successo (Verrà cancellata anche dai libri)")
        #La categoria viene cancellata anche da tutti i libri nel database
        # che la contengono
        return
    else:
        print("Categoria non trovata")
        return
    
    
def stampa_categorie():
    """
    Permette di visualizzare tutte le categorie
    presenti nel database.
    """
    with open('categorie.csv', 'r', newline = '') as file:
        categorie = csv.reader(file)
        print('')
        for row in categorie:
            print(', '.join(row))