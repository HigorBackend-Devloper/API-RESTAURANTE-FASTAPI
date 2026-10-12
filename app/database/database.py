import sqlite3
from contextlib import contextmanager


class Banco_de_dados:
    def __init__(self, nome_arquivo="restaurante.db"):
        self.nome_arquivo = nome_arquivo
        self.init_database()

    @contextmanager
    def conectar(self):
        conexao = sqlite3.connect(self.nome_arquivo)
        conexao.execute("PRAGMA foreign_keys = ON")
        try:
            yield conexao
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def init_database(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS restaurantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    ativo INTEGER NOT NULL DEFAULT 1,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conexao.commit()
