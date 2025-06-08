import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

HOST = 'localhost'
PORT = 15000

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Cliente")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((HOST, PORT))
        except:
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor.")
            master.quit()
            return

        self.nome = simpledialog.askstring("Login", "Digite seu nome de usuário:", parent=self.master)
        self.socket.send(self.nome.encode('utf-8'))
        self.senha = simpledialog.askstring("Senha", "Digite sua senha:", parent=self.master, show='*')
        self.socket.send(self.senha.encode('utf-8'))

        resposta = self.socket.recv(1024).decode('utf-8')
        if "Senha incorreta" in resposta:
            messagebox.showerror("Erro", resposta)
            self.socket.close()
            master.quit()
            return

        self.janela_chat()

        threading.Thread(target=self.receber_mensagens, daemon=True).start()

    def janela_chat(self):
        self.txt_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.txt_area.pack(padx=10, pady=10)

        self.entry_dest = tk.Entry(self.master, width=30)
        self.entry_dest.pack(padx=10, pady=5)
        self.entry_dest.insert(0, "/listar")

        self.entry_msg = tk.Entry(self.master, width=60)
        self.entry_msg.pack(padx=10, pady=5)
        self.entry_msg.bind("<Return>", lambda event: self.enviar())

        self.btn_send = tk.Button(self.master, text="Enviar", command=self.enviar)
        self.btn_send.pack(pady=5)

        self.btn_sair = tk.Button(self.master, text="Sair", command=self.sair)
        self.btn_sair.pack(pady=5)

    def enviar(self):
        destinatario = self.entry_dest.get().strip()
        mensagem = self.entry_msg.get().strip()
        if destinatario == "" or mensagem == "":
            return

        try:
            self.socket.send(destinatario.encode('utf-8'))
            if destinatario.lower() != "/sair":
                self.socket.send(mensagem.encode('utf-8'))
            self.entry_msg.delete(0, tk.END)
        except:
            self.exibir_mensagem("Erro ao enviar mensagem.")

    def receber_mensagens(self):
        while True:
            try:
                mensagem = self.socket.recv(1024).decode('utf-8')
                if mensagem:
                    self.exibir_mensagem(mensagem)
            except:
                break

    def exibir_mensagem(self, mensagem):
        self.txt_area.config(state='normal')
        self.txt_area.insert(tk.END, mensagem + "\n")
        self.txt_area.config(state='disabled')
        self.txt_area.see(tk.END)

    def sair(self):
        try:
            self.socket.send("/sair".encode('utf-8'))
            self.socket.close()
        except:
            pass
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
