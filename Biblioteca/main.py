import sys
import Prestiti
import Libri
import Categorie
import Utenti


def menu():
    """
    Menù principale della biblioteca.
    Da qui è possibile accedere al menù prestiti, libri,
    categorie e utenti.
    """
    print('\nA quale menù vuoi accedere?')
    choice = input('P. Menù Prestiti\nL. Menù Libri\nC. Menù Categorie\nU. Menù Utenti\nE. Esci\n--> ').upper()
    while True:
        if choice.upper() == 'P':
            Prestiti.menu_prestiti()
        if choice.upper() == 'L':
            Libri.menu_libri()
        if choice.upper() == 'C':
            Categorie.menu_categorie()
        if choice.upper() == 'U':
            Utenti.menu_utenti()
        if choice.upper() == 'E':
            sys.exit()
        else:
            choice = input("Inserisci un valore valido: ")


if __name__ == '__main__':
    menu()