import socket
import threading
import sqlite3
from datetime import datetime

# Configurações
HOST = 'localhost'
PORT = 15000
DB_PATH = 'data/chat.db'
clientes = {}  # socket: nome

# Função para conectar ao banco
def get_db_connection():
    return sqlite3.connect(DB_PATH)

# Envia mensagem para um cliente específico
def enviar_para_cliente(destinatario, mensagem):
    for cliente, nome in clientes.items():
        if nome == destinatario:
            cliente.send(mensagem.encode('utf-8'))
            return True
    return False

# Envia mensagem para todos (menos o remetente)
def broadcast(mensagem, remetente=None):
    for cliente in clientes:
        if cliente != remetente:
            cliente.send(mensagem.encode('utf-8'))

# Gerencia cada cliente
def handle_client(client_socket):
    try:
        client_socket.send("Digite seu nome de usuário: ".encode('utf-8'))
        nome = client_socket.recv(1024).decode('utf-8').strip()

        client_socket.send("Digite sua senha: ".encode('utf-8'))
        senha = client_socket.recv(1024).decode('utf-8').strip()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE nome=?", (nome,))
        user = cur.fetchone()

        if user:
            if user[2] != senha:
                client_socket.send("Senha incorreta. Conexão encerrada.".encode('utf-8'))
                client_socket.close()
                return
        else:
            cur.execute("INSERT INTO usuarios (nome, senha, online) VALUES (?, ?, 1)", (nome, senha))
            conn.commit()

        # Marcar como online
        cur.execute("UPDATE usuarios SET online = 1 WHERE nome = ?", (nome,))
        conn.commit()
        conn.close()

        clientes[client_socket] = nome
        broadcast(f"{nome} entrou no chat.", remetente=client_socket)
        print(f"{nome} conectado.")

        # Enviar mensagens offline
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT remetente, mensagem FROM mensagens_offline WHERE destinatario = ?", (nome,))
        for remetente, mensagem in cur.fetchall():
            client_socket.send(f"[Offline] {remetente}: {mensagem}".encode('utf-8'))
        cur.execute("DELETE FROM mensagens_offline WHERE destinatario = ?", (nome,))
        conn.commit()
        conn.close()

        while True:
            client_socket.send("Digite o destinatário (/listar ou /sair): ".encode('utf-8'))
            destinatario = client_socket.recv(1024).decode('utf-8').strip()

            if destinatario.lower() == "/sair":
                break
            elif destinatario.lower() == "/listar":
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT nome, online FROM usuarios")
                lista = [f"{n} ({'online' if o else 'offline'})" for n, o in cur.fetchall()]
                conn.close()
                client_socket.send("Usuários:
".encode('utf-8') + "
".join(lista).encode('utf-8'))
                continue

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE nome = ?", (destinatario,))
            if not cur.fetchone():
                client_socket.send("Usuário não encontrado.
".encode('utf-8'))
                conn.close()
                continue

            client_socket.send("Digite sua mensagem: ".encode('utf-8'))
            mensagem = client_socket.recv(1024).decode('utf-8').strip()

            if not enviar_para_cliente(destinatario, f"{nome} ➡ {destinatario}: {mensagem}"):
                cur.execute("INSERT INTO mensagens_offline (remetente, destinatario, mensagem) VALUES (?, ?, ?)", (nome, destinatario, mensagem))
                conn.commit()
                client_socket.send("Usuário offline. Mensagem armazenada.
".encode('utf-8'))
            conn.close()

    except Exception as e:
        print(f"Erro com {clientes.get(client_socket, 'desconhecido')}: {e}")

    finally:
        nome = clientes.get(client_socket, "desconhecido")
        print(f"{nome} saiu.")
        clientes.pop(client_socket, None)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET online = 0 WHERE nome = ?", (nome,))
        conn.commit()
        conn.close()
        broadcast(f"{nome} saiu do chat.")
        client_socket.close()

# Inicia o servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Servidor iniciado em", HOST, ":", PORT)

while True:
    client_socket, _ = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
