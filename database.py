import sqlite3
import os


DATABASE = "data/apresentacao.db"


def conectar():

    os.makedirs("data", exist_ok=True)

    conexao = sqlite3.connect(DATABASE)

    conexao.row_factory = sqlite3.Row

    return conexao


def inicializar_banco():

    conexao = conectar()

    cursor = conexao.cursor()


    # ==========================================
    # APRESENTAÇÕES
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS apresentacoes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,

            descricao TEXT,

            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # ==========================================
    # SLIDES
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slides (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            apresentacao_id INTEGER NOT NULL,

            titulo TEXT,

            texto TEXT,

            tamanho INTEGER DEFAULT 60,

            cor_texto TEXT DEFAULT '#ffffff',

            cor_fundo TEXT DEFAULT '#000000',

            alinhamento TEXT DEFAULT 'center',

            ordem INTEGER DEFAULT 0,

            FOREIGN KEY (
                apresentacao_id
            )
            REFERENCES apresentacoes(id)

        )
    """)


    conexao.commit()

    conexao.close()


# Inicializa automaticamente
inicializar_banco()