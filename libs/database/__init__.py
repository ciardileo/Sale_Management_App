# imports

from tkinter import *
import sqlite3 as sql
from csv import *


# função que remodela o banco novamente caso precisar

def db_products_model(cur, con):
    model = 'create table products(' \
            '   id integer primary key autoincrement not null,' \
            '   name varchar(100) not null,' \
            '   EAN int(13) not null,' \
            '   value char(9) not null,' \
            '   quantity int(6)' \
            ');'

    cur.execute(model)

    con.commit()

    con.close()


def db_clients_model(cur, con):
    model = 'create table clients(' \
            '   id integer primary key autoincrement not null,' \
            '   name varchar(80) not null,' \
            '   email varchar(30) not null,' \
            '   phone char(14)' \
            ');'

    cur.execute(model)

    con.commit()

    con.close()


def set_data(con, cur, csv):
    reader1 = reader(csv)

    prods = list(reader1)

    for item in prods:
        data = item[0].split(';')

        command = 'insert into products(EAN, name, value, quantity) values (?, ?, ?, 0)'
        inst = (data[0], data[1], data[2] + '.00')

        print(data)
        cur.execute(command, inst)

        con.commit()

    csv.close()
    con.close()
