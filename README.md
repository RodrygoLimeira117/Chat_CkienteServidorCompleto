
# Chat Cliente/Servidor em Python

Este projeto implementa um sistema de chat com arquitetura **Cliente/Servidor** utilizando **Python**, **Tkinter** e **SQLite**. Desenvolvido como parte da disciplina de **Redes de Computadores** no curso de Engenharia da Computação (UFRPE).

## 📌 Funcionalidades

### Servidor (`server/serverChat.py`)
- Registro e login de usuários com nome e senha
- Validação de autenticação usando banco de dados SQLite
- Controle de status online/offline dos usuários
- Armazenamento e entrega de mensagens offline
- Conexão simultânea de múltiplos clientes via `threading`
- Comandos `/listar` (listar usuários) e `/sair` (desconectar)

### Cliente com GUI (`client/clientChatGUI.py`)
- Interface gráfica com **Tkinter**
- Janela de login com nome de usuário e senha
- Campo de envio e recebimento de mensagens
- Lista de usuários com status online/offline (com comando `/listar`)
- Suporte a múltiplas conversas com diferentes usuários

## 🗃️ Banco de Dados (`data/chat.db`)
- Tabela `usuarios`: armazena credenciais e status
- Tabela `mensagens_offline`: mensagens aguardando destinatários que estavam offline

## 🛠️ Como executar

### 1. Iniciar o servidor
```bash
cd server
python serverChat.py
```

### 2. Iniciar o cliente
```bash
cd client
python clientChatGUI.py
```

⚠️ Certifique-se de que o servidor está em execução antes de abrir o cliente.

## 📁 Estrutura de Pastas

```
chat_app_completo/
│
├── server/
│   └── serverChat.py
│
├── client/
│   └── clientChatGUI.py
│
├── data/
│   └── chat.db
```

## 📚 Créditos

Desenvolvido por **José Rodrigo Araújo Limeira**, estudante de Engenharia da Computação na UFRPE.  
Professor: *Ygor Amaral Barbosa Leite de Sena*  
Projeto da disciplina: *Redes de Computadores*

---

**Divirta-se programando e aprendendo sobre redes! 🚀**
