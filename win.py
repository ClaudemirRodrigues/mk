from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import sqlite3
import requests
import awesometkinter as atk
import test


def Tk():
    pass


window = tk.Tk()


class Functions:
    # Função para retornar os dados com base no CEP
    def cep_search(self):
        cep = self.entry_cep.get()
        if len(cep) != 8:
            print('\033[31mFormato inválido!\033[m')
            messagebox.showinfo('ALERTA', 'Formato inválido!\nTente novamente.')
            self.entry_cep.delete(0, END)

        request = requests.get(f'https://viacep.com.br/ws/{cep}/json/')

        address_data = request.json()

        # Loop para auto completar os campos
        if 'erro' not in address_data:
            self.entry_adress.delete(0, END)
            self.entry_adress.insert(0, address_data['logradouro'])
            self.entry_adress.insert(len(address_data['logradouro']), ' - ' + address_data['bairro'])
            self.entry_city.delete(0, END)
            self.entry_city.insert(0, address_data['localidade'])
            self.entry_uf.delete(0, END)
            self.entry_uf.insert(0, address_data['uf'])
        else:
            messagebox.showinfo('ALERTA', 'CEP não encontrado!\nTente novamente.')
            self.entry_cep.delete(0, END)

    # Função para limpr os campos
    def clear_screen(self):
        self.entry_code.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_phone.delete(0, END)
        self.entry_city.delete(0, END)
        self.entry_cep.delete(0, END)
        self.entry_adress.delete(0, END)
        self.entry_birthday.delete(0, END)
        self.entry_number.delete(0, END)
        self.entry_uf.delete(0, END)

    def connect_db(self):
        self.connect = sqlite3.connect('.clientes.db')
        self.cursor = self.connect.cursor()
        print('Conectando...')

    def disconnect_db(self):
        self.connect.close()
        print('Banco desconectado')

    def createTables(self):
        self.connect_db()
        # Cria tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                endereco CHAR(60),
                cidade CHAR(20),
                uf CHAR(2),
                telefone INTEGER(20)
            );
        """)
        self.connect.commit()
        print('Banco criado')
        self.disconnect_db()

    def addClient(self):
        self.code = self.entry_code.get()
        self.name = self.entry_name.get()
        self.adress = self.entry_adress.get()
        self.city = self.entry_city.get()
        self.phone = self.entry_phone.get()
        self.uf = self.entry_uf.get()

        self.connect_db()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, endereco, cidade, uf, telefone)
            VALUES (?, ?, ?, ?, ?)""", (self.name, self.adress, self.city, self.uf, self.phone))
        self.connect.commit()
        self.disconnect_db()
        self.selectList()
        self.clear_screen()

    def selectList(self):
        self.listClient.delete(*self.listClient.get_children())
        self.connect_db()
        data_list = self.cursor.execute(""" SELECT cod, nome_cliente, endereco, cidade, uf, telefone FROM clientes
            ORDER BY nome_cliente ASC; """)

        for i in data_list:
            self.listClient.insert("", END, values=i)
        self.disconnect_db()


class Application(Functions):
    def __init__(self):
        self.window = window
        self.screen()
        self.frames()
        self.widgets()
        self.frame2_list()
        self.createTables()
        self.selectList()
        window.mainloop()

    def screen(self):
        self.window.title('Cadastro de Clientes Mary Kay')
        self.window.configure(background='#f3dde7')
        self.window.geometry('900x700')
        self.window.resizable(True, True)
        self.window.maxsize(width=900, height=700)
        self.window.minsize(width=600, height=500)

    def frames(self):
        self.frame_1 = atk.Frame3d(self.window, bg='#f3dde7')
        self.frame_1.place(relx=.02, rely=.02, relwidth=.96, relheight=.46)

        self.frame_2 = atk.Frame3d(self.window, bg='#fcdde7')
        self.frame_2.place(relx=.02, rely=.5, relwidth=.96, relheight=.48)

    def widgets(self):
        global endereco
        # Botão Limpar
        self.bt_clear = atk.Button3d(self.frame_1, text='Limpar',
                               bg='#fcdde7', fg='white', command=self.clear_screen)
        self.bt_clear.place(relx=.2, rely=.05, relwidth=.1, relheight=.12)
        # Botão Buscar
        self.bt_search = atk.Button3d(self.frame_1, text='Buscar',
                               bg='#fcdde7')
        self.bt_search.place(relx=.3, rely=.05, relwidth=.1, relheight=.12)
        # Botão Novo
        self.bt_new = atk.Button3d(self.frame_1, text='Novo',
                               bg='#fcdde7', command=self.addClient)
        self.bt_new.place(relx=.6, rely=.05, relwidth=.1, relheight=.12)
        # Botão Alterar
        self.bt_change = atk.Button3d(self.frame_1, text='Alterar',
                               bg='#fcdde7')
        self.bt_change.place(relx=.7, rely=.05, relwidth=.1, relheight=.12)
        # Botão Apagar
        self.bt_del = atk.Button3d(self.frame_1, text='Apagar',
                               bg='#fcdde7')
        self.bt_del.place(relx=.8, rely=.05, relwidth=.1, relheight=.12)

        """# Botão Apagar
        self.bt_del = Button(self.frame_1, text='Apagar', bd=2,
                             bg='#da70d6', fg='white', font=('ubuntu', 10))
        self.bt_del.place(relx=.8, rely=.05, relwidth=.1, relheight=.12)"""

        # Label e entrada do Código
        self.lb_code = Label(self.frame_1, text='Código', bg='#f3dde7', fg='#0c2218')
        self.lb_code.place(relx=.05, rely=.04)
        self.entry_code = Entry(self.frame_1, relief='groove')
        self.entry_code.place(relx=.05, rely=.1, relwidth=.08, relheight=.07)

        # Label e entrada do Nome
        self.lb_name = Label(self.frame_1, text='Nome', bg='#f3dde7', fg='#0c2218')
        self.lb_name.place(relx=.05, rely=.19)
        self.entry_name = Entry(self.frame_1, relief='groove')
        self.entry_name.place(relx=.05, rely=.25, relwidth=.7, relheight=.07)

        # Label e entrada do aniversário
        self.lb_birthday =Label(self.frame_1, text='Aniversário', bg='#f3dde7', fg='#0c2218')
        self.lb_birthday.place(relx=.8, rely=.19)
        self.entry_birthday = Entry(self.frame_1, relief='groove')
        self.entry_birthday.place(relx=.8, rely=.25, relwidth=.1, relheight=.07)

        # Label e entrada do CEP
        self.lb_cep = Label(self.frame_1, text='CEP', bg='#f3dde7', fg='#0c2218')
        self.lb_cep.place(relx=.05, rely=.34)
        self.entry_cep = Entry(self.frame_1, relief='groove')
        self.entry_cep.place(relx=.05, rely=.4, relwidth=.1, relheight=.07)
        # Botão para fazer a chamada da função cep_search
        self.bt_cep = Button(self.frame_1, text='Buscar\nCEP', bd=1,
                               bg='#fcdde7', fg='black', font=('ubuntu', 7), command=self.cep_search)
        self.bt_cep.place(relx=.15, rely=.40, relwidth=.05, relheight=.07)

        # Label e entrada do endereço
        self.lb_adress = Label(self.frame_1, text='Endereço', bg='#f3dde7', fg='#0c2218')
        self.lb_adress.place(relx=.2, rely=.34)
        self.entry_adress = Entry(self.frame_1, relief='groove')
        self.entry_adress.place(relx=.2, rely=.4, relwidth=.55, relheight=.07)

        # Label e entrada do número da residência
        self.lb_number = Label(self.frame_1, text='Número', bg='#f3dde7', fg='#0c2218')
        self.lb_number.place(relx=.8, rely=.34)
        self.entry_number = Entry(self.frame_1, relief='groove')
        self.entry_number.place(relx=.8, rely=.4, relwidth=.1, relheight=.07)

        # Label e entrada da Cidade
        self.lb_city = Label(self.frame_1, text='Cidade', bg='#f3dde7', fg='#0c2218')
        self.lb_city.place(relx=.05, rely=.49)
        self.entry_city = Entry(self.frame_1, relief='groove')
        self.entry_city.place(relx=.05, rely=.55, relwidth=.4, relheight=.07)

        # Label e entrada do Estado
        self.lb_uf = Label(self.frame_1, text='UF', bg='#f3dde7', fg='#0c2218')
        self.lb_uf.place(relx=.5, rely=.49)
        self.entry_uf = Entry(self.frame_1, relief='groove')
        self.entry_uf.place(relx=.5, rely=.55, relwidth=.1, relheight=.07)

        # Label e entrada do Email

        # Label e entrada do telefone
        self.lb_phone = Label(self.frame_1, text='Telefone', bg='#f3dde7', fg='#0c2218')
        self.lb_phone.place(relx=.5, rely=.64)
        self.entry_phone = Entry(self.frame_1, relief='groove')
        self.entry_phone.place(relx=.5, rely=.7, relwidth=.4, relheight=.07)



    def frame2_list(self):
        self.listClient = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'))
        self.listClient.heading('#0', text='')
        self.listClient.heading('#1', text='Código')
        self.listClient.heading('#2', text='Nome')
        self.listClient.heading('#3', text='Endereço')
        self.listClient.heading('#4', text='Cidade')
        self.listClient.heading('#5', text='UF')
        self.listClient.heading('#6', text='Telefone')

        self.listClient.column('#0', width=0)
        self.listClient.column('#1', width=0)  # Código
        self.listClient.column('#2', width=150)  # Nome
        self.listClient.column('#3', width=260)  # Endereço
        self.listClient.column('#4', width=60)  # Cidade
        self.listClient.column('#5', width=0)  # UF
        self.listClient.column('#6', width=30)  # Telefone

        self.listClient.place(relx=.01, rely=.1, relwidth=.95, relheight=.85)

        self.scroolList = Scrollbar(self.frame_2, orient='vertical')
        self.listClient.configure(yscroll=self.scroolList.set)
        self.scroolList.place(relx=.96, rely=.1, relwidth=.025, relheight=.85)


Application()
