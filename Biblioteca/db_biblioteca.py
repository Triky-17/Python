import sqlite3


def create():
    """
    Crea il database "biblioteca" e le tabelle
    "Prestiti", "Libri", "Utenti", "Categorie"
    e "Autori" in sqlite3
    """
    
    db_biblioteca = 'biblioteca.sqlite'
    conn = sqlite3.connect(db_biblioteca)
    conn.close()
    
    
    conn = sqlite3.connect('file:biblioteca.sqlite?mode=rw', uri=True)
    conn.execute("pragma foreign_keys = 1") # Rimedio a malfunzionamento foreign keys
    cur = conn.cursor()
    
    
    Autori_sql = """
        create table if not exists Autori (
            nome           varchar(255) not null,
            cognome        varchar(255) not null,
            data_nascita   date not null,  
            luogo_nascita  varchar(255) not null,
            note           text,
            unique (nome, cognome));"""
    cur.execute(Autori_sql)
    
    
    Categorie_sql = """
        create table if not exists Categorie (
            categoria      varchar(255) primary key);"""
    cur.execute(Categorie_sql)
    
    
    Libri_sql = """
        create table if not exists Libri (
            isbn           integer primary key,  
            titolo         varchar(255) not null,
            lingua         varchar(255) not null,
            editore        varchar(255) not null,
            anno           date not null,
            categorie      varchar(255) not null,
            numero_copie   integer not null,
            autori         varchar(255) not null);"""
    cur.execute(Libri_sql)
    
    Utenti_sql = """
        create table if not exists Utenti (
            tessera        integer primary key autoincrement,
            nome           varchar(255) not null,
            cognome        varchar(255) not null,
            data_reg       date not null,
            telefono       varchar(255) not null,
            indirizzo      varchar(255) not null,
            email          varchar(255));"""
    cur.execute(Utenti_sql)
    
    Prestiti_sql = """
        create table if not exists Prestiti (
            id_prestito    integer primary key autoincrement,
            data_inizio    date not null,
            data_fine      date not null,
            isbn_libro     integer not null,
            libro          varchar(255) not null,
            tessera_utente integer not null,
            utente         varchar(255) not null,
            data_consegna  date not null,
            tipo_ritardo   varchar(255) not null,
            foreign key (isbn_libro) references Libri(isbn) on delete cascade,
            foreign key (tessera_utente) references Utenti(tessera) on delete cascade);"""
            # Foreign keys inserite per permettere la cancellazione di un prestito
            # quando un libro o un utente ad esso associati vengono rimossi
    cur.execute(Prestiti_sql)
    
    
    conn.commit()
    conn.close()
    
    
create()
