import customtkinter as ctk
from tkinter import *
import sqlite3 as sq
from tkinter import messagebox


class BackEnd():
    def conectadb(self):
        self.con = sq.connect("sistema_users.db")
        self.cursor = self.con.cursor()
        print("Banco de dados conectado com sucesso!")

    def desconectadb(self):
        self.cursor.close()
        self.con.close()
        print("Banco de dados foi desconectado")

    def criar_tabela(self):
        self.conectadb()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                login TEXT NOT NULL,
                                senha TEXT NOT NULL,
                                cfrmsenha TEXT NOT NULL);''')

        self.con.commit()

        print("Tabela criada com sucesso!")

        self.desconectadb()

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.password_cadastro = self.password_cadastro_entry.get()
        self.confirm_cadastro = self.confirm_cadastro_entry.get()

        self.conectadb()

        self.cursor.execute('''INSERT INTO usuarios (username, login, senha, cfrmsenha) VALUES (?, ?, ?, ?)''', (
            self.username_cadastro, self.email_cadastro, self.password_cadastro, self.confirm_cadastro))

        try:

            if (self.username_cadastro == "" or self.email_cadastro == "" or self.password_cadastro == "" or self.confirm_cadastro == ""):
                messagebox.showerror(
                    title="Sistema de login", message="Por favor preencha todos os campos!")

            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(
                    title="Sistema de login", message="O nome do usuário deve conter pelo menos 4 caracteres.")

            elif (len(self.password_cadastro) < 4):
                messagebox.showwarning(
                    title="Sistema de login", message="A senha do usuário deve conter pelo menos 4 caracteres.")

            elif (self.password_cadastro != self.confirm_cadastro):
                messagebox.showerror(
                    title="Sistema de login", message="As senhas não são iguais. Por favor tente novamente!")

            else:
                self.con.commit()
                self.limpaEntryCadastro()
                messagebox.showinfo(
                    "Sistema de login", message=f"Parabéns {self.username_cadastro}!\nCadastro realizado com sucesso!")
                self.desconectadb()

        except:
            messagebox.showinfo(
                "Sistema de login", message=f"Erro no processamento do seu cadastro!\nPor favor tente novamente!")
            self.desconectadb()

    def verify_login(self):
        self.email_login = self.email_login_entry.get()
        self.password_login = self.password_login_entry.get()

        self.conectadb()

        self.cursor.execute('''SELECT * FROM usuarios WHERE (login = ? and senha = ?)''',
                            (self.email_login, self.password_login))

        self.verifica_dados = self.cursor.fetchone()

        try:
            if (self.email_login == "" or self.password_login == ""):
                messagebox.showerror(
                    title="Sistema de Login", message="Preencha todas os campos!")

            elif (self.email_login in self.verifica_dados and self.password_login in self.verifica_dados):
                messagebox.showinfo(
                    title="Sistema de Login", message="Seja bem vindo!\nLogin realizado com sucesso!")
                self.desconectadb()
                self.limpaEntryLogin()

        except:
            messagebox.showerror(
                title="Sistema de Login", message="Credencias não cadastradas no sistema.\nVerifique os dados ou cadastra-se!")
            self.desconectadb()


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoesJanelaInicial()
        self.telaLogin()
        self.criar_tabela()

    def configuracoesJanelaInicial(self):
        self.geometry("700x400")
        self.title("Tela de Login")
        self.resizable(False, False)

    def telaLogin(self):

        # inserindo a imagem e configurando
        self.img = PhotoImage(file='img.png')
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=5)

        # Ajuste no texto interno da janela
        self.title = ctk.CTkLabel(
            self, text="Realize seu login ou cadastre-se\n para acesso aos serviços!", font=("Futura Md Bt bold", 18))
        self.title.grid(row=0, column=0, pady=10, padx=10)

        # Frame do formulário
        self.frame_login = ctk.CTkFrame(self, width=400, height=500)
        self.frame_login.place(x=350, y=10)

        # Inserção do widgets no frame
        self.lb_title = ctk.CTkLabel(
            self.frame_login, text="Faça o seu login", font=("Futura Md Bt bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        # Input do login de acesso do usuário
        self.email_login_entry = ctk.CTkEntry(
            self.frame_login, width=300, placeholder_text="Login do usuário", font=("Futura Md Bt", 16), corner_radius=20, border_color="white")
        self.email_login_entry.grid(row=1, column=0, padx=10, pady=10)

        # Input da senha do usuário
        self.password_login_entry = ctk.CTkEntry(
            self.frame_login, width=300, placeholder_text="Senha do usuário", font=("Futura Md Bt", 16), corner_radius=20, border_color="white", show="*")
        self.password_login_entry.grid(row=2, column=0, padx=10, pady=10)

        # Checkbox de visualização da senha
        self.checkbox_login_entry = ctk.CTkCheckBox(
            self.frame_login, text="Mostrar a senha", font=("Futura Md Bt", 12), corner_radius=10, border_color="white", command=self.showEntrySenha)
        self.checkbox_login_entry.grid(row=3, column=0, padx=10, pady=10)

        # Botão de acesso ao sistema
        self.btn_login_entry = ctk.CTkButton(
            self.frame_login, width=300, hover_color="#012", text="Acessar".upper(), font=("Futura Md Bt bold", 14), corner_radius=20, command=self.verify_login)
        self.btn_login_entry.grid(row=4, column=0, padx=10, pady=10)

        # Texto de cadastro ao sistema
        self.sap = ctk.CTkLabel(self.frame_login, text="Caso não seja cadastro, clique no botão abaixo", font=(
            "Futura Md Bt bold", 12))
        self.sap.grid(row=5, column=0, padx=10, pady=10)

        # Área de cadastro ao sistema
        self.btn_register_entry = ctk.CTkButton(
            self.frame_login, width=300, fg_color="#196", hover_color="#999", text="Fazer cadastro".upper(), font=("Futura Md Bt bold", 14), corner_radius=20, command=self.telaCadastro)
        self.btn_register_entry.grid(row=6, column=0, padx=10, pady=10)

    def telaCadastro(self):
        # Remover formulário de login
        self.frame_login.place_forget()

        # Inserção do widgets no frame
        self.frame_cadastro = ctk.CTkFrame(self, width=400, height=500)
        self.frame_cadastro.place(x=350, y=10)

        # Criando o texto de login do cadastro
        self.lb_title = ctk.CTkLabel(
            self.frame_cadastro, text="Faça o seu login", font=("Futura Md Bt bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=5)

        # Input de nome de cadastro de usuário
        self.username_cadastro_entry = ctk.CTkEntry(
            self.frame_cadastro, width=300, placeholder_text="Nome do usuário", font=("Futura Md Bt", 16), corner_radius=20, border_color="white")
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        # Input de email de cadastro de usuário
        self.email_cadastro_entry = ctk.CTkEntry(
            self.frame_cadastro, width=300, placeholder_text="Email do usuário", font=("Futura Md Bt", 16), corner_radius=20, border_color="white")
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        # Input de password de cadastro de usuário
        self.password_cadastro_entry = ctk.CTkEntry(
            self.frame_cadastro, width=300, placeholder_text="Senha", font=("Futura Md Bt", 16), corner_radius=20, border_color="white", show="*")
        self.password_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)

        # Input de confirma password de cadastro de usuário
        self.confirm_cadastro_entry = ctk.CTkEntry(
            self.frame_cadastro, width=300, placeholder_text="Confirma senha", font=("Futura Md Bt", 16), corner_radius=20, border_color="white", show="*")
        self.confirm_cadastro_entry.grid(row=4, column=0, padx=10, pady=5)

        # Checkbox de visualização da senha de cadatro
        self.checkbox_cadastro_entry = ctk.CTkCheckBox(
            self.frame_cadastro, text="Mostrar a senha", font=("Futura Md Bt", 12), corner_radius=10, border_color="white")
        self.checkbox_cadastro_entry.grid(row=5, column=0, pady=5)

        # Botão de confirmar cadastro ao sistema
        self.btn_cadastro_user = ctk.CTkButton(
            self.frame_cadastro, width=300, fg_color="#196", hover_color="#999",  text="Confirmar cadastro".upper(), font=("Futura Md Bt bold", 14), corner_radius=20, command=self.cadastrar_usuario)
        self.btn_cadastro_user.grid(row=6, column=0, padx=10, pady=5)

        # Botão de voltar ao login
        self.btn_cadastro_user = ctk.CTkButton(
            self.frame_cadastro, width=300, fg_color="#889", hover_color="#333", text="<- Voltar ao login".upper(), font=("Futura Md Bt bold", 14), corner_radius=20, command=self.telaLogin)
        self.btn_cadastro_user.grid(row=7, column=0, padx=10, pady=5)

    def limpaEntryCadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.password_cadastro_entry.delete(0, END)
        self.confirm_cadastro_entry.delete(0, END)

    def limpaEntryLogin(self):
        self.email_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

    def showEntrySenha(self):

        if (self.checkbox_login_entry_var.get() == 1):
            self.password_login_entry.configure(show='')
        else:
            self.password_login_entry.configure(show='*')


if __name__ == '__main__':
    app = App()
    app.mainloop()
