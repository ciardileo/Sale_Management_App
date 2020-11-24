'''
Projeto Sistema de Vendas
Fase:
Completo ( )
'''


# imports

from libs.menus import *
from tkinter import *
import sqlite3 as sql

# classe que contém a inicialização do aplicativo
class App:
    def __init__(self):

        # janela

        self.main = Tk()
        self.main.title('Sistema de Vendas')
        self.main.geometry('1100x800')
        self.main.resizable(0, 0)

        # conexão com o banco de dados

        self.con = sql.connect('produtos.db')

        # cursor do banco de dados

        self.cur = self.con.cursor()

        # arquivo csv dos produtos

        self.csv = open('Products2.csv', 'r')

        # ícone de configuração

        self.config_icon = PhotoImage(file='imagens/gear_icon.png')


        # interface gráfica
        
        UI(self.main, self.config_icon, self.con, self.cur)

        self.main.mainloop()


if __name__ == '__main__':
    App()

print('teste')

print('leonardo lopes ciardi')
