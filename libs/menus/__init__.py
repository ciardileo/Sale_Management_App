# imports

from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import *
import os
from libs.database import *


# classe que contém todas as funções

class UI:
    def __init__(self, main, icon_config, con, cur):

        # caminho atual

        self.app_path = os.path.dirname(os.path.realpath(__file__))

        print(self.app_path)

        # ícones

        self.sale_icon = PhotoImage(
            file=os.path.join(self.app_path.replace("menus", ""), 'imagens', 'sales_icon.png'))

        self.refresh_icon = PhotoImage(
            file=os.path.join(self.app_path.replace("menus", ""), 'imagens', 'refresh-icon.png'))

        # fontes

        self.font1 = 'Helvetica 18'
        self.font2 = 'Helvetica 14'
        self.font3 = 'Helvetica 12'

        # cores

        self.blue = "#0079d3"

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

        self.lb_cod = Label(self.sale_frame, text='Código EAN do Produto:', font=self.font1)

        self.ean_cod = Entry(self.sale_frame, font=self.font1)

        # nome do produto

        self.lb_name = Label(self.sale_frame, text='Nome do Produto:', font=self.font1)

        self.product_name = Entry(self.sale_frame, font=self.font1)

        # quantidade do produto

        self.lb_qtt = Label(self.sale_frame, text='Quantidade do Produto', font=self.font1)

        self.product_quantity = Scale(self.sale_frame, from_=1, to=40, orient=HORIZONTAL, font=self.font1)

        # botão de registrar

        self.register_button = Button(self.sale_frame, text='Registrar', command=self.register, bg=self.blue,
                                      relief='flat', fg='white', font=self.font2)

        # botão de resetar

        self.reset_button = Button(self.sale_frame, text='Resetar', command=self.sale_reset, bg=self.blue,
                                   relief='flat', fg='white', font=self.font2)

        # aba products =============================================================================================

        self.products_frame = Frame(self.main, height=730, width=1100)

        # botões de gerenciamento do banco de dados

        self.reset_sales_bt = Button(self.products_frame, text='Resetar Vendas', bg=self.blue, relief='flat',
                                     fg='white', font=self.font2, command=self.reset_sales)

        self.delete_product_bt = Button(self.products_frame, text='Remover Produto', bg=self.blue, relief='flat',
                                        fg='white', font=self.font2, command=self.delete_product)

        self.edit_product_bt = Button(self.products_frame, text='Editar Produto', bg=self.blue, relief='flat',
                                      fg='white', font=self.font2, command=self.edit_product)

        self.add_product_bt = Button(self.products_frame, text='Adicionar Produto', bg=self.blue, relief='flat',
                                     fg='white', font=self.font2, command=self.add_product)

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

        self.search_bar = Entry(self.search_frame, font=self.font3)

        # variável que conterá o que a pessoa quer pesquisar

        self.search_parameter = StringVar()

        # radio buttons para o que a pessoa quer pesquisar

        self.lb_radio = Label(self.search_frame, text='Pesquisar por:', font=self.font3)

        self.search_p1 = Radiobutton(self.search_frame, text='Nome do Produto', variable=self.search_parameter,
                                     value='name', font=self.font3)
        self.search_p2 = Radiobutton(self.search_frame, text='ID', variable=self.search_parameter, value='id',
                                     font=self.font3)
        self.search_p3 = Radiobutton(self.search_frame, text='EAN', variable=self.search_parameter, value='EAN',
                                     font=self.font3)
        self.search_p4 = Radiobutton(self.search_frame, text='Preço', variable=self.search_parameter, value='value',
                                     font=self.font3)
        self.search_p5 = Radiobutton(self.search_frame, text='Quantidade', variable=self.search_parameter,
                                     value='quantity', font=self.font3)

        # botão pesquisar

        self.bt_search = Button(self.search_frame, text='Pesquisar', command=self.search, bg=self.blue, relief='flat',
                                fg='white', font=self.font2)

        # botão resetar

        self.reset_search_button = Button(self.search_frame, text='Resetar', command=self.reset_search_results,
                                          bg=self.blue, relief='flat', fg='white', font=self.font2)

        # label que mostrará a quantidade de resultados da pesquisa

        self.results_qtt = Label(self.search_frame, font=self.font3)

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

        self.title_lb = Label(self.config_frame, text='Configurações', font=self.font1)

        self.lb_register_way = Label(self.config_frame, text='Registrar produto por:', font=self.font2)

        self.register_way = StringVar()

        self.EAN_way = Radiobutton(self.config_frame, text='Código EAN', variable=self.register_way, value='EAN',
                                   font=self.font3)
        self.name_way = Radiobutton(self.config_frame, text='Nome do produto', variable=self.register_way, value='name',
                                    font=self.font3)

        self.EAN_way.select()
        self.register_way.set('EAN')

        # aba clients ===================================================

        self.clients_frame = Frame(self.main)

        self.add_lb = Label(self.clients_frame, text='Cadastrar cliente', font=self.font3)

        self.client_name_lb = Label(self.clients_frame, text='Nome:', font=self.font3)
        self.client_name_entry = Entry(self.clients_frame, font=self.font3)

        self.client_email_lb = Label(self.clients_frame, text='Email:', font=self.font3)
        self.client_email_entry = Entry(self.clients_frame, font=self.font3)

        self.client_phone_lb = Label(self.clients_frame, text='Número:', font=self.font3)
        self.client_phone_entry = Entry(self.clients_frame, font=self.font3)

        self.register_client_button = Button(self.clients_frame, text='Adicionar Cliente', command=self.register_client,
                                             bg=self.blue, relief='flat', fg='white', font=self.font2)

        self.reset_client_button = Button(self.clients_frame, text='Resetar', command=self.reset_clients_data,
                                          bg=self.blue, relief='flat', fg='white', font=self.font2)

        self.refresh_clients_button = Button(self.clients_frame, image=self.refresh_icon, command=self.refresh_clients,
                                             relief='flat', fg='white', font=self.font2)

        self.clients_tree_frame = Frame(self.clients_frame, pady=20)

        # scrollbar

        self.tree_scroll3 = Scrollbar(self.clients_tree_frame)

        # tabela que mostrará os clientes

        self.clients_tree = ttk.Treeview(self.clients_tree_frame, yscrollcommand=self.tree_scroll3.set,
                                         selectmode='browse', height=200)
        self.tree_scroll3.config(command=self.clients_tree.yview)

        self.clients_tree['columns'] = ('ID', 'Nome', 'Email', 'Telefone')

        # formatando as colunas

        self.clients_tree.column('#0', width=0, stretch=NO)
        self.clients_tree.column('ID', anchor=CENTER, width=60, minwidth=15)
        self.clients_tree.column('Nome', anchor=W, width=250)
        self.clients_tree.column('Email', width=250)
        self.clients_tree.column("Telefone", anchor=W, width=250)

        # cabeçalho da tabela

        self.clients_tree.heading('ID', text='ID')
        self.clients_tree.heading('Nome', text='Nome')
        self.clients_tree.heading('Email', text='Email')
        self.clients_tree.heading('Telefone', text='Telefone')

        # aba reports ==============================================================

        # frame da aba

        self.report_frame = Frame(self.main)

        # label da comissão

        self.comission_lb = Label(self.report_frame, text='Porcentagem de comissão:', font=self.font1)

        # entry da comissão

        self.comission_entry = Entry(self.report_frame, font=self.font2)

        # botão de calcular comissão

        self.comission_button = Button(self.report_frame, text='Calcular', command=self.comission, bg=self.blue,
                                       relief='flat', fg='white', font=self.font2)

        # label de resposta

        self.comission_total = Label(self.report_frame, text='Sua Comissão: R$', font=self.font2, fg='green')

        # meta do vendedor

        self.goal_lb = Label(self.report_frame, text='Meta:', font=self.font1)

        self.goal_entry = Entry(self.report_frame, font=self.font2)

        self.goal_button = Button(self.report_frame, text='Calcular', command=self.goal, bg=self.blue, relief='flat',
                                  fg='white', font=self.font2)

        self.goal_status_lb = Label(self.report_frame, font=self.font2)

        # gerar planilha

        self.spreadsheet_bt = Button(self.report_frame, text='Gerar Planilha De Vendas',
                                     command=self.generate_spreadsheet, bg=self.blue, relief='flat', fg='white',
                                     font=self.font2)

        # aba estatísticas ================================================================================

        self.statistics_frame = Frame(self.main)

        # self.wip_label = Label(self.statistics_frame, text='Está aba ainda não está pronta! Volte mais tarde.', font='Helveltica 30 bold')
        #
        # self.ico_warning = PhotoImage(file=os.path.join(self.app_path.replace("menus", ""), 'imagens', 'warning-icon.png'))
        # self.warning_icon = Label(self.statistics_frame, image=self.ico_warning)

        self.most_sold_products = Button(self.statistics_frame, text='Mais vendidos', font=self.font2,
                                         command=self.most_sold)
        self.most_expensive_product = Button(self.statistics_frame, text='Mais caros', font=self.font2,
                                             command=self.most_expensive)
        self.most_cheap_product = Button(self.statistics_frame, text='Mais baratos', font=self.font2,
                                         command=self.most_cheap)

        # table frame

        self.statistics_table_frame = Frame(self.statistics_frame)

        # scrollbar

        self.statistics_table_scroll = Scrollbar(self.statistics_table_frame)

        self.statistics_table = ttk.Treeview(self.statistics_table_frame,
                                             yscrollcommand=self.statistics_table_scroll.set, selectmode='browse',
                                             height=25)

        self.statistics_table_scroll.config(command=self.statistics_table.yview)

        self.statistics_table['columns'] = ('ID', 'Nome', 'EAN', 'Preço', 'Quantidade')

        # formatando as colunas

        self.statistics_table.column('#0', width=0, stretch=NO)
        self.statistics_table.column('ID', anchor=CENTER, width=60, minwidth=15)
        self.statistics_table.column('Nome', anchor=W, width=350)
        self.statistics_table.column('EAN', width=270)
        self.statistics_table.column("Preço", anchor=W, width=140)
        self.statistics_table.column('Quantidade', anchor=CENTER, width=100, minwidth=15)

        # cabeçalho da tabela

        self.statistics_table.heading('ID', text='ID')
        self.statistics_table.heading('Nome', text='Nome')
        self.statistics_table.heading('EAN', text='EAN')
        self.statistics_table.heading('Preço', text='Preço')
        self.statistics_table.heading('Quantidade', text='Quantidade')

        self.view_in_graphics_bt = Button(self.statistics_frame, text='Ver em gráfico', bg=self.blue, relief='flat',
                                          fg='white', font=self.font2)

        self.actual_view = str()

        # executando os métodos

        # db_clients_model(self.cur, self.con)

        self.header()

    # função do cabeçalho

    def header(self):

        self.top_frame.pack()

        # config button

        self.bt_config = Button(self.top_frame, image=self.icon_config, borderwidth=0, bg='#D9D9D9',
                                command=self.config_tab)
        self.bt_config.place(x=1010, y=17)

        # abas

        self.tab_sales = Button(self.top_frame, text='VENDAS', height=5, width=10, borderwidth=0,
                                command=self.sale_register)
        self.tab_sales.place(x=55, y=0)

        self.tab_clients = Button(self.top_frame, text='CLIENTES', height=5, width=10, borderwidth=0,
                                  command=self.clients_tab)
        self.tab_clients.place(x=190, y=0)

        self.tab_products = Button(self.top_frame, text='PRODUTOS', height=5, width=10, borderwidth=0,
                                   command=self.products_tab)
        self.tab_products.place(x=325, y=0)

        self.tab_reports = Button(self.top_frame, text='RELATÓRIOS', height=5, width=10, borderwidth=0,
                                  command=self.reports_tab)
        self.tab_reports.place(x=450, y=0)

        self.tab_statistics = Button(self.top_frame, text='ESTATÍSTICAS', height=5, width=10, borderwidth=0,
                                     command=self.statistics_tab)
        self.tab_statistics.place(x=575, y=0)

        self.tab_search = Button(self.top_frame, text='BUSCAR', height=5, width=10, borderwidth=0,
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
            # if self.ean_cod1.isnumeric() == False:
            #    pass

            # if len(self.ean_cod1) < 13:
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

        self.products_frame.pack(fill=BOTH)

        self.reset_sales_bt.pack(pady=5)
        self.delete_product_bt.pack()
        self.edit_product_bt.pack(pady=5)
        self.add_product_bt.pack()

        for record in self.table.get_children():
            self.table.delete(record)

        # empacotamentos

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

    def reset_sales(self):

        command = 'update products set quantity = 0 where quantity >= 1'

        self.cur.execute(command)

        self.con.commit()

    def selectItem(self):
        selected = self.table.focus()

        return self.table.item(selected)

    def edit_product(self):

        product = self.selectItem()

        print(product)

        if len(product['values']) <= 1:
            pass
        else:
            product = product['values']

            popup = Toplevel()

            lb_name = Label(popup, text='Nome do Produto:', font=self.font3)
            entry_name = Entry(popup, font=self.font3)
            lb_name.grid(row=1, column=1)
            entry_name.grid(row=1, column=2)

            lb_ean = Label(popup, text='Código EAN:', font=self.font3)
            entry_ean = Entry(popup, font=self.font3)
            lb_ean.grid(row=2, column=1)
            entry_ean.grid(row=2, column=2)

            lb_price = Label(popup, text='Preço:', font=self.font3)
            entry_price = Entry(popup, font=self.font3)
            lb_price.grid(row=3, column=1)
            entry_price.grid(row=3, column=2)

            lb_quantity = Label(popup, text='Quantidade Vendida:', font=self.font3)
            entry_quantity = Entry(popup, font=self.font3)
            lb_quantity.grid(row=4, column=1)
            entry_quantity.grid(row=4, column=2)

            entry_name.insert(0, product[1])
            entry_ean.insert(0, product[2])
            entry_price.insert(0, str(product[3]).replace('.', ','))
            entry_quantity.insert(0, product[4])

            def update():

                new_name = str(entry_name.get())
                new_ean = int(entry_ean.get())
                new_price = str(entry_price.get()).replace(',', '.')
                new_quantity = int(entry_quantity.get())

                command = 'update products set name = ?, EAN = ?, value = ?, quantity = ? where id = ?'

                self.cur.execute(command, (new_name, new_ean, new_price, new_quantity, product[0]))

                self.con.commit()

                popup.destroy()

            def reset():
                entry_name.delete(0, END)
                entry_ean.delete(0, END)
                entry_price.delete(0, END)
                entry_quantity.delete(0, END)

            update_bt = Button(popup, text='Atualizar', fg='white', bg=self.blue, font=self.font3, command=update)
            reset_bt = Button(popup, text='Resetar Campos', fg='white', bg=self.blue, font=self.font3, command=reset)
            cancel_bt = Button(popup, text='Cancelar', fg='white', bg=self.blue, font=self.font3, command=popup.destroy)

            update_bt.grid(row=5, column=1, pady=5, padx=5)
            reset_bt.grid(row=5, column=2, pady=5, padx=5)
            cancel_bt.grid(row=5, column=3, pady=5, padx=5)

            popup.mainloop()

    def delete_product(self):

        product = self.selectItem()
        product = product['values']

        print(product)

        command = 'delete from products where id = ?'

        id = product[0]

        self.cur.execute(command, (id,))

        # self.con.commit()

    def add_product(self):

        popup = Toplevel()

        lb_name = Label(popup, text='Nome do Produto:', font=self.font3)
        entry_name = Entry(popup, font=self.font3)
        lb_name.grid(row=1, column=1)
        entry_name.grid(row=1, column=2)

        lb_ean = Label(popup, text='Código EAN:', font=self.font3)
        entry_ean = Entry(popup, font=self.font3)
        lb_ean.grid(row=2, column=1)
        entry_ean.grid(row=2, column=2)

        lb_price = Label(popup, text='Preço:', font=self.font3)
        entry_price = Entry(popup, font=self.font3)
        lb_price.grid(row=3, column=1)
        entry_price.grid(row=3, column=2)

        lb_quantity = Label(popup, text='Quantidade Vendida:', font=self.font3)
        entry_quantity = Entry(popup, font=self.font3)
        lb_quantity.grid(row=4, column=1)
        entry_quantity.grid(row=4, column=2)

        entry_quantity.insert(0, '0')

        def add():
            name = str(entry_name.get())
            ean = int(entry_ean.get())
            price = str(entry_price.get()).replace(',', '.')
            quantity = int(entry_quantity.get())

            command = 'insert into products (name, EAN, value, quantity) values (?, ?, ?, ?)'

            self.cur.execute(command, (name, ean, price, quantity))

            self.con.commit()

            popup.destroy()

        def reset():
            entry_name.delete(0, END)
            entry_ean.delete(0, END)
            entry_price.delete(0, END)
            entry_quantity.delete(0, END)

        update_bt = Button(popup, text='Adicionar', fg='white', bg=self.blue, font=self.font3, command=add)
        reset_bt = Button(popup, text='Resetar Campos', fg='white', bg=self.blue, font=self.font3, command=reset)
        cancel_bt = Button(popup, text='Cancelar', fg='white', bg=self.blue, font=self.font3, command=popup.destroy)

        update_bt.grid(row=5, column=1, pady=5, padx=5)
        reset_bt.grid(row=5, column=2, pady=5, padx=5)
        cancel_bt.grid(row=5, column=3, pady=5, padx=5)

        popup.mainloop()

    # aba search =====================================================================================================

    def search_tab(self):

        # limpando a tela

        self.clean_screen()

        # empacotamentos

        self.search_frame.pack()

        self.search_bar.pack(pady=8)

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
            count += 1
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

        self.config_frame.pack(pady=5)

        self.title_lb.pack(pady=5)

        self.lb_register_way.pack(pady=5)

        self.EAN_way.pack(pady=5)
        self.name_way.pack(pady=5)

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
        self.refresh_clients_button.place(x=750, y=180)

        self.refresh_clients()

    def reset_clients_data(self):
        self.client_name_entry.delete(0, END)
        self.client_email_entry.delete(0, END)
        self.client_phone_entry.delete(0, END)

    def register_client(self):
        try:

            self.new_client_name = str(self.client_name_entry.get())
            self.new_client_email = str(self.client_email_entry.get())
            self.new_client_phone = str(self.client_phone_entry.get())

            command = 'insert into clients (name, email, phone) values (?, ?, ?)'

            self.cur.execute(command, (self.new_client_name, self.new_client_email, self.new_client_phone))

            self.con.commit()

            messagebox.showinfo('IMPORTANTE!', message='NOVO CLIENTE REGISTRADO')

            self.reset_clients_data()

        except:
            messagebox.showinfo('IMPORTANTE!', message='UM ERRO OCORREU!')

    def refresh_clients(self):

        for record in self.clients_tree.get_children():
            self.clients_tree.delete(record)

        command = 'select * from clients'

        self.cur.execute(command)

        clients_db = self.cur.fetchall()

        self.con.commit()

        id = 1

        for client in clients_db:
            self.clients_tree.insert(parent='', index='end', iid=id,
                                     values=(client[0], client[1], client[2], client[3]))
            id += 1

    # aba reports

    def reports_tab(self):

        # limpa a tela

        self.clean_screen()

        # empacotamentos

        self.report_frame.pack()

        self.comission_lb.pack(pady=5)

        self.comission_entry.pack(pady=5)

        self.comission_button.pack(pady=5)

        self.comission_total.pack(pady=5)

        self.goal_lb.pack(pady=5)

        self.goal_entry.pack(pady=5)

        self.goal_button.pack(pady=5)

        self.goal_status_lb.pack(pady=5)

        self.spreadsheet_bt.pack(pady=5)

    # função que calcula a comissõa

    def comission(self):

        command = 'select value, quantity from products where quantity >=1'

        self.cur.execute(command)

        values = self.cur.fetchall()

        self.con.commit()

        print(values)

        valor_final = 0

        for value in values:
            valor_final += float(value[0]) * value[1]

        comission = self.comission_entry.get().replace(',', '.')

        print(valor_final)

        valor_final = (float(comission.replace('%', ' ')) / 100) * valor_final

        valor_final = str(round(valor_final, 2)).replace('.', ',')

        self.comission_total['text'] = f'Sua Comissão: R${valor_final}'

    # função que calcula a meta

    def goal(self):

        self.cur.execute('select value, quantity from products where quantity >=1')

        values = self.cur.fetchall()

        self.con.commit()

        meta = self.goal_entry.get().replace(',', '.')

        meta = meta.replace('R$', ' ')

        meta = int(meta)

        valor_final = 0

        for value in values:
            valor_final += float(value[0]) * value[1]

        # meta = valor_final * 100 / int(meta)

        if valor_final < meta:

            difference = round(meta - valor_final)

            self.goal_status_lb['text'] = f'Ainda faltam R${str(difference).replace(".", ",")} para alcançar sua meta'
            self.goal_status_lb['fg'] = 'red'

        elif valor_final > meta:

            difference = round(valor_final - meta)

            self.goal_status_lb['text'] = f'Você ultrapassou a meta em R${str(difference).replace(".", ",")}!!!'
            self.goal_status_lb['fg'] = 'green'

        else:

            self.goal_status_lb['text'] = 'Você bateu a meta!'
            self.goal_status_lb['fg'] = 'yellow'

    # função que gera a planilha

    def generate_spreadsheet(self):

        file = asksaveasfilename(filetypes=(('CSV files', '*.csv'),))

        if file:

            with open(f'{file}.csv', 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, dialect=excel, delimiter=',')

                csv_writer.writerow(('ID', 'Nome', 'EAN', 'Preco', 'Quantidade'))

                self.cur.execute('select * from products')

                data_base = self.cur.fetchall()

                self.con.commit()

                for product in data_base:
                    csv_writer.writerow(product)

                csv_file.close()

                messagebox.showinfo('IMPORTANTE!',
                                    message='O ARQUIVO FOI SALVO COMO CSV! CONFIGURE O EXCEL PARA VER OS DADOS CORRETAMENTE')

    # função que empacota a aba statistics

    def statistics_tab(self):

        self.clean_screen()

        self.statistics_frame.pack(fill=BOTH)

        self.most_expensive_product.pack()
        self.most_sold_products.pack()
        self.most_cheap_product.pack()

        self.view_in_graphics_bt.pack(pady=15)

        self.statistics_table_frame.pack()

        self.statistics_table_scroll.pack(side=RIGHT, fill=Y)

        self.statistics_table.pack()

    def most_sold(self):
        self.actual_view = 'most sold'

        for record in self.statistics_table.get_children():
            self.statistics_table.delete(record)

        self.cur.execute('select * from products')
        products = self.cur.fetchall()
        self.con.commit()

        quantity = list()

        for x in products:
            quantity.append(x[4])

        quantity.sort(reverse=True)

        most_sold = list()
        count = 0

        for n in range(1, 6):
            most_sold.append(quantity[count])
            count += 1

        print(most_sold)

        # c = Counter(most_sold)
        # print(c)

        # print(most_sold.index(15))

        self.cur.execute('select * from products where value = ? or ? or ? or ? or ?', most_sold)
        final = self.cur.fetchall()
        self.con.commit()
        print(final)

        final = sorted(sorted(final, key=lambda x: x[4]), key=lambda x: x[4], reverse=True)

        print(final)

        id = 1

        sorted_p = list()

        for i in range(0, 5):
            sorted_p.append(final[i])

        print(sorted_p)

        for product in sorted_p:
            self.statistics_table.insert(parent='', index='end', iid=id,
                                         values=(product[0], product[1], product[2], product[3], product[4]))
            id += 1

        def graphic_view():
            names = list()
            sales = list()

            for p in sorted_p:
                names.append(str(p[0]))
                sales.append(p[4])

            plt.bar(names, sales)
            plt.xlabel('Produtos por ID')
            plt.ylabel('Vendas')
            plt.title('Produtos mais vendidos')
            plt.show()

        self.view_in_graphics_bt.config(command=graphic_view)

    def most_expensive(self):
        self.actual_view = 'most expensive'

        for record in self.statistics_table.get_children():
            self.statistics_table.delete(record)

        self.cur.execute('select * from products')
        products = self.cur.fetchall()
        self.con.commit()

        value = list()

        for x in products:
            value.append(x[3])

        value = list(map(lambda x: float(x), value))

        value.sort(reverse=True)

        most_expensive = list()
        count = 0

        for n in range(1, 6):
            most_expensive.append(value[count])
            count += 1

        print(most_expensive)

        # c = Counter(most_sold)
        # print(c)

        # print(most_expensive.index(15))

        self.cur.execute('select * from products where value = ? or ? or ? or ? or ?', most_expensive)
        a = list(self.cur.fetchall())
        final = list()
        for x in a:
            final.append([x[0], x[1], x[2], float(x[3]), x[4]])

        self.con.commit()
        print(final)

        final = sorted(sorted(final, key=lambda x: x[3]), key=lambda x: x[3], reverse=True)

        print(final)

        id = 1

        sorted_p = list()

        for i in range(0, 5):
            sorted_p.append(final[i])

        print(sorted_p)

        for product in sorted_p:
            self.statistics_table.insert(parent='', index='end', iid=id,
                                         values=(product[0], product[1], product[2], product[3], product[4]))
            id += 1

        def graphic_view():
            names = list()
            sales = list()

            for p in sorted_p:
                names.append(str(p[0]))
                sales.append(p[3])

            plt.bar(names, sales)
            plt.xlabel('Produtos por ID')
            plt.ylabel('Preço')
            plt.title('Produtos mais caros')
            plt.show()

        self.view_in_graphics_bt.config(command=graphic_view)

    def most_cheap(self):
        self.actual_view = 'most cheap'

        for record in self.statistics_table.get_children():
            self.statistics_table.delete(record)

        self.cur.execute('select * from products')
        products = self.cur.fetchall()
        self.con.commit()

        value = list()

        for x in products:
            value.append(x[3])

        value = list(map(lambda x: float(x), value))

        value.sort()

        most_cheap = list()
        count = 0

        for n in range(1, 6):
            most_cheap.append(value[count])
            count += 1

        print(most_cheap)

        # c = Counter(most_sold)
        # print(c)

        # print(most_expensive.index(15))

        self.cur.execute('select * from products where value = ? or ? or ? or ? or ?', most_cheap)
        a = list(self.cur.fetchall())
        final = list()
        for x in a:
            final.append([x[0], x[1], x[2], float(x[3]), x[4]])

        self.con.commit()
        print(final)

        final = sorted(sorted(final, key=lambda x: x[3]), key=lambda x: x[3])

        print(final)

        id = 1

        sorted_p = list()

        for i in range(0, 5):
            sorted_p.append(final[i])

        print(sorted_p)

        for product in sorted_p:
            self.statistics_table.insert(parent='', index='end', iid=id,
                                         values=(product[0], product[1], product[2], product[3], product[4]))
            id += 1

        def graphic_view():
            names = list()
            sales = list()

            for p in sorted_p:
                names.append(str(p[0]))
                sales.append(p[3])

            plt.bar(names, sales)
            plt.xlabel('Produtos por ID')
            plt.ylabel('Preço')
            plt.title('Produtos mais baratos')
            plt.show()

        self.view_in_graphics_bt.config(command=graphic_view)

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

        # limpando a aba reports

        self.report_frame.pack_forget()

        # limpando a aba statistics

        self.statistics_frame.pack_forget()
