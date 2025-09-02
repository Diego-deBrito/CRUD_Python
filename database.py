"""
Módulo de banco de dados.
Responsável por criar a tabela e fornecer funções CRUD (Create, Read, Update, Delete).
Usa SQLite por simplicidade, mas pode ser adaptado para PostgreSQL ou MySQL.
"""

import sqlite3

# Nome do arquivo do banco de dados
DB_NAME = "cadastros.db"


def init_db():
    """Inicializa o banco de dados e cria a tabela se não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()


def inserir(nome, email):
    """Insere um novo registro no banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pessoas (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    conn.close()


def listar():
    """Lista todos os registros da tabela pessoas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    rows = cursor.fetchall()
    conn.close()
    return rows


def atualizar(id_, nome, email):
    """Atualiza um registro existente pelo ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE pessoas SET nome=?, email=? WHERE id=?", (nome, email, id_))
    conn.commit()
    conn.close()


def deletar(id_):
    """Remove um registro pelo ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pessoas WHERE id=?", (id_,))
    conn.commit()
    conn.close()
