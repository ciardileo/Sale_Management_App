# imports

from tkinter import messagebox
from tkinter import ttk

from libs.database import *


# classe que contém todas as funções

class UI:
    def __init__(self, main, icon_config, con, cur):

        # ícones

        self.sale_icon = PhotoImage(file='C:/Users/Léo/PycharmProjects/Gerenciamento De Vendas/libs/imagens/sales_icon.png')

        # instâncias

        self.main = main
        self.icon_config = icon_config
        self.con = con
        self.cur = cur

        # frames das abas

        # frame do cabeçalho

        self.top_frame = Frame(self.main, bg='#D9D9D9', height=70, width=1100)

        # aba de vendas ========================================================

        self.sale_frame = Frame(self.main, height=730, width=1100)

        # código EAN do produto

        self.lb_cod = Label(self.sale_frame, text='Código EAN do Produto:', font='Arial 15')

        self.ean_cod = Entry(self.sale_frame, font='Arial 15')

        # nome do produto

        self.lb_name = Label(self.sale_frame, text='Nome do Produto:', font='Arial 15')

        self.product_name = Entry(self.sale_frame, font='Arial 15')

        # quantidade do produto

        self.lb_qtt = Label(self.sale_frame, text='Quantidade do Produto', font='Arial 15')

        self.product_quantity = Scale(self.sale_frame, from_=1, to=40, orient=HORIZONTAL, font='Arial 15')

        # botão de registrar

        self.register_button = Button(self.sale_frame, text='REGISTRAR', command=self.register, font='Arial 15', relief="flat",bg='#0079d3', fg='white')

        # botão de resetar

        self.reset_button = Button(self.sale_frame, text='RESETAR', command=self.sale_reset, font='Arial 15', relief="flat",bg='#0079d3', fg='white')

        # aba products =============================================================================================

        self.products_frame = Frame(self.main, height=730, width=1100)

        # criando um frame para a o treeview

        self.tree_frame = Frame(self.products_frame, pady=50, height=730)

        # scrollbar do treeview

        self.tree_scroll = Scrollbar(self.tree_frame)

        # tabela que mostrará os produtos

        self.table = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode='browse', height=730)
        self.tree_scroll.config(command=self.table.yview)

        self.table['columns'] = ('ID', 'Nome', 'EAN', 'Preço', 'Quantidade')

        # formatando as colunas

        self.table.column('#0', width=0, stretch=NO)
        self.table.column('ID', anchor=CENTER, width=60, minwidth=15)
        self.table.column('Nome', anchor=W, width=400)
        self.table.column('EAN', width=200)
        self.table.column("Preço", anchor=W, width=200)
        self.table.column('Quantidade', anchor=CENTER, width=90)

        # cabeçalho da tabela

        self.table.heading('ID', text='ID')
        self.table.heading('Nome', text='Nome')
        self.table.heading('EAN', text='EAN')
        self.table.heading('Preço', text='Preço')
        self.table.heading('Quantidade', text='Quantidade')

        # aba search=============================================================================

        # frame de pesquisa

        self.search_frame = Frame(self.main)

        # barra de pesquisa

        self.search_bar = Entry(self.search_frame)

        # variável que conterá o que a pessoa quer pesquisar

        self.search_parameter = StringVar()

        # radio buttons para o que a pessoa quer pesquisar

        self.lb_radio = Label(self.search_frame, text='Pesquisar por:')

        self.search_p1 = Radiobutton(self.search_frame, text='Nome do Produto', variable=self.search_parameter,
                                     value='name')
        self.search_p2 = Radiobutton(self.search_frame, text='ID', variable=self.search_parameter, value='id')
        self.search_p3 = Radiobutton(self.search_frame, text='EAN', variable=self.search_parameter, value='EAN')
        self.search_p4 = Radiobutton(self.search_frame, text='Preço', variable=self.search_parameter, value='value')
        self.search_p5 = Radiobutton(self.search_frame, text='Quantidade', variable=self.search_parameter,
                                     value='quantity')

        # botão pesquisar

        self.bt_search = Button(self.search_frame, text='Pesquisar', command=self.search, relief="flat",bg='#0079d3', fg='white')

        # botão resetar

        self.reset_search_button = Button(self.search_frame, text='Resetar', command=self.reset_search_results, relief="flat",bg='#0079d3', fg='white')

        # label que mostrará a quantidade de resultados da pesquisa

        self.results_qtt = Label(self.search_frame)

        # frame da tabela que mostrará os resultados da pesquisa

        self.search_tree_frame = Frame(self.search_frame, pady=50, height=650)

        # scrollbar do treeview

        self.tree_scroll2 = Scrollbar(self.search_tree_frame)

        # tabela que mostrará os produtos

        self.search_tree = ttk.Treeview(self.search_tree_frame, yscrollcommand=self.tree_scroll2.set,
                                        selectmode='browse', height=400)
        self.tree_scroll2.config(command=self.search_tree.yview)

        self.search_tree['columns'] = ('ID', 'Nome', 'EAN', 'Preço', 'Quantidade')

        # formatando as colunas

        self.search_tree.column('#0', width=0, stretch=NO)
        self.search_tree.column('ID', anchor=CENTER, width=60, minwidth=15)
        self.search_tree.column('Nome', anchor=W, width=400)
        self.search_tree.column('EAN', width=200)
        self.search_tree.column("Preço", anchor=W, width=200)
        self.search_tree.column('Quantidade', anchor=CENTER, width=90)

        # cabeçalho da tabela

        self.search_tree.heading('ID', text='ID')
        self.search_tree.heading('Nome', text='Nome')
        self.search_tree.heading('EAN', text='EAN')
        self.search_tree.heading('Preço', text='Preço')
        self.search_tree.heading('Quantidade', text='Quantidade')

        # aba options =================================================

        self.config_frame = Frame(self.main)

        self.title_lb = Label(self.config_frame, text='Configurações')

        self.lb_register_way = Label(self.config_frame, text='Registrar prodruto por:')

        self.register_way = StringVar()

        self.EAN_way = Radiobutton(self.config_frame, text='Código EAN', variable=self.register_way, value='EAN')
        self.name_way = Radiobutton(self.config_frame, text='Nome do produto', variable=self.register_way, value='name')

        self.EAN_way.select()
        self.register_way.set('EAN')

        # aba clients ===================================================

        self.clients_frame = Frame(self.main)

        self.add_lb = Label(self.clients_frame, text='Cadastrar cliente')

        self.client_name_lb = Label(self.clients_frame, text='Nome:')
        self.client_name_entry = Entry(self.clients_frame)

        self.client_email_lb = Label(self.clients_frame, text='Email:')
        self.client_email_entry = Entry(self.clients_frame)

        self.client_phone_lb = Label(self.clients_frame, text='Número:')
        self.client_phone_entry = Entry(self.clients_frame)

        self.register_client_button = Button(self.clients_frame, text='Adicionar Cliente')

        self.reset_client_button = Button(self.clients_frame, text='Resetar')

        self.clients_tree_frame = Frame(self.clients_frame, pady=20)

        # scrollbar

        self.tree_scroll3 = Scrollbar(self.clients_tree_frame)

        # tabela que mostrará os clientes

        self.clients_tree = ttk.Treeview(self.clients_tree_frame, yscrollcommand=self.tree_scroll3.set, selectmode='browse', height=200)
        self.tree_scroll3.config(command=self.clients_tree.yview)

        self.clients_tree['columns'] = ('ID', 'Nome', 'Email', 'Telefone')

        # formatando as colunas

        self.clients_tree.column('#0', width=0, stretch=NO)
        self.clients_tree.column('ID', anchor=CENTER, width=60, minwidth=15)
        self.clients_tree.column('Nome', anchor=W, width=400)
        self.clients_tree.column('Email', width=200)
        self.clients_tree.column("Telefone", anchor=W, width=200)

        # cabeçalho da tabela

        self.clients_tree.heading('ID', text='ID')
        self.clients_tree.heading('Nome', text='Nome')
        self.clients_tree.heading('Email', text='Email')
        self.clients_tree.heading('Telefone', text='Telefone')

        # executando os métodos

        # db_clients_model(self.cur, self.con)

        self.header()

    # função do cabeçalho

    def header(self):

        self.top_frame.pack()

        # config button

        self.bt_config = Button(self.top_frame, image=self.icon_config, borderwidth=0, bg='#D9D9D9', command=self.config_tab)
        self.bt_config.place(x=1010, y=17)

        # abas

        self.tab_sales = Button(self.top_frame, text='PRODUCTS', height=5, width=10 , borderwidth=0,
                                command=self.sale_register)
        self.tab_sales.place(x=55, y=0)

        self.tab_clients = Button(self.top_frame, text='CLIENTS', height=5, width=10, borderwidth=0, command=self.clients_tab)
        self.tab_clients.place(x=190, y=0)

        self.tab_products = Button(self.top_frame, text='PRODUCTS', height=5, width=10, borderwidth=0,
                                   command=self.products_tab)
        self.tab_products.place(x=325, y=0)

        self.tab_products = Button(self.top_frame, text='REPORTS', height=5, width=10, borderwidth=0)
        self.tab_products.place(x=450, y=0)

        self.tab_statistics = Button(self.top_frame, text='STATISTICS', height=5, width=10, borderwidth=0)
        self.tab_statistics.place(x=575, y=0)

        self.tab_search = Button(self.top_frame, text='SEARCH', height=5, width=10, borderwidth=0,
                                 command=self.search_tab)
        self.tab_search.place(x=700, y=0)

    # aba de registro de venda================================================================================

    def sale_register(self):

        # limpa a tela

        self.clean_screen()

        # empacotamentos

        self.sale_frame.pack()

        if self.register_way.get() == 'EAN':
            self.lb_name.pack_forget()
            self.product_name.pack_forget()
            self.lb_cod.pack()
            self.ean_cod.pack()
        else:
            self.lb_cod.pack_forget()
            self.ean_cod.pack_forget()
            self.lb_name.pack()
            self.product_name.pack()

        self.lb_qtt.pack()
        self.product_quantity.pack()
        self.register_button.pack(pady=10)
        self.reset_button.pack(pady=10)

    # reseta os campos

    def sale_reset(self):
        self.ean_cod.delete(0, END)
        self.product_name.delete(0, END)
        self.product_quantity.set(0)

    # registra a venda no banco de dados

    def register(self):

        # armazenando dados em variáveis

        self.ean_cod1 = self.ean_cod.get()

        self.product_name2 = self.product_name.get()

        self.product_quantity2 = self.product_quantity.get()

        if self.register_way.get() == 'EAN':
            self.value = self.ean_cod1
            self.command = 'select quantity from products where EAN = ?'
            self.command2 = 'update products set quantity = ? where EAN = ?'
        else:
            self.value = self.product_name2
            self.command = 'select quantity from products where name = ?'
            self.command2 = 'update products set quantity = ? where name = ?'

        # pegando a quantidade do produto vendida no banco de dados


        self.cur.execute(self.command, (self.value,))

        self.actual_value = self.cur.fetchall()

        self.final_value = self.actual_value[0]

        self.product_quantity2 += self.final_value[0]

        # regisrtrando a venda no banco de dados

        try:

            print(self.product_quantity2)
            #if self.ean_cod1.isnumeric() == False:
            #    pass

            #if len(self.ean_cod1) < 13:
             #   pass

            # inserindo dados na tabela

            self.insts = (self.product_quantity2, self.value)

            self.cur.execute(self.command2, self.insts)

            self.con.commit()

            messagebox.showinfo('IMPORTANTE!', message='REGISTRO DE VENDA ADICIONADO COM SUCESSO!')

        except:

            messagebox.showinfo('AVISO!', message='UM ERRO OCORREU!')

        finally:

            self.sale_reset()

    # aba Products ==================================================================================================

    def products_tab(self):

        # limpa a tela

        self.clean_screen()

        for record in self.table.get_children():
            self.table.delete(record)

        # empacotamentos

        self.products_frame.pack()
        self.tree_frame.pack()
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        self.table.pack(fill=Y)

        # armazenando os produtos em uma lista

        self.cur.execute('select * from products')

        self.products = self.cur.fetchall()

        self.con.commit()

        # print(self.products)

        # passando os produtos para a tabela

        id = 1

        for self.line in self.products:
            self.table.insert(parent='', index='end', iid=id,
                              values=(self.line[0], self.line[1], self.line[2], self.line[3], self.line[4]))
            id += 1

    # aba search =====================================================================================================

    def search_tab(self):

        # limpando a tela

        self.clean_screen()

        # empacotamentos

        self.search_frame.pack()

        self.search_bar.pack()

        self.lb_radio.pack()

        self.search_p1.pack()
        self.search_p2.pack()
        self.search_p3.pack()
        self.search_p4.pack()
        self.search_p5.pack()

        self.bt_search.pack(pady=10)

        self.reset_search_button.pack(pady=10)

        self.results_qtt.pack()

        self.search_tree_frame.pack()

        self.tree_scroll2.pack(side=RIGHT, fill=Y)

        self.search_tree.pack()

    def search(self):

        print(self.search_parameter.get())

        self.parameter = self.search_parameter.get()

        self.parameter2 = f'{self.search_bar.get()}%'

        if self.parameter == 'id':
            self.command2 = 'select * from products where id like ?'
            self.parameter2 = f'{self.search_bar.get()}'

        if self.parameter == 'EAN':
            self.command2 = 'select * from products where EAN like ?'

        if self.parameter == 'name':
            self.command2 = 'select * from products where name like ?'

        if self.parameter == 'value':
            self.command2 = 'select * from products where value like ?'

        if self.parameter == 'quantity':
            self.command2 = 'select * from products where quantity like ?'
            self.parameter2 = f'{self.search_bar.get()}'


        self.cur.execute(self.command2, (self.parameter2,))

        self.search_results = self.cur.fetchall()

        self.con.commit()

        print(self.search_results)

        self.reset_search_results()

        count = 0
        for line in self.search_results:
            count+=1
            self.search_tree.insert(parent='', index='end',
                              values=(line[0], line[1], line[2], line[3], line[4]))

        self.results_qtt['text'] = f'{str(count)} resultado(s) encontrado(s):'


    # função que reseta a tabela

    def reset_search_results(self):
        for record in self.search_tree.get_children():
            self.search_tree.delete(record)
            self.results_qtt['text'] = '0 resultado(s) encontrado(s):'


    def config_tab(self):

        self.clean_screen()

        self.config_frame.pack()

        self.title_lb.pack()

        self.lb_register_way.pack()

        self.EAN_way.pack()
        self.name_way.pack()

    def clients_tab(self):

        self.clean_screen()

        self.clients_frame.pack()
        self.add_lb.pack()
        self.client_name_lb.pack()
        self.client_name_entry.pack()
        self.client_email_lb.pack()
        self.client_email_entry.pack()
        self.client_phone_lb.pack()
        self.client_phone_entry.pack()
        self.register_client_button.pack(padx=10, pady=10)
        self.reset_client_button.pack()
        self.clients_tree_frame.pack()
        self.tree_scroll3.pack(side=RIGHT, fill=Y)
        self.clients_tree.pack()

    # função que limpa a tela

    def clean_screen(self):

        # limpando a aba sales

        self.sale_frame.pack_forget()

        # limpando a aba products

        self.products_frame.pack_forget()

        # limpando a aba search

        self.search_frame.pack_forget()

        # limpando a aba configurações

        self.config_frame.pack_forget()

        # limpando a aba clients

        self.clients_frame.pack_forget()
