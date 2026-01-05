import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('investimentos.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        self.popular_dados()
    
    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                perfil TEXT DEFAULT 'conservador'
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS investimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                perfil_minimo TEXT NOT NULL,
                rentabilidade REAL NOT NULL,
                vencimento_dias INTEGER
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_investimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                investimento_id INTEGER,
                valor REAL NOT NULL,
                data_investimento TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def popular_dados(self):
        investimentos = [
            ('CDB Banco X', 'renda_fixa', 'conservador', 12.5, 180),
            ('Tesouro Selic', 'renda_fixa', 'conservador', 11.8, 365),
            ('Ações Petrobras', 'renda_variavel', 'moderado', 15.0, 0),
            ('Fundo Imobiliário XP', 'fundo', 'moderado', 10.5, 90),
            ('Tesouro IPCA+', 'renda_fixa', 'moderado', 13.2, 730)
        ]
        
        self.cursor.executemany(
            'INSERT OR IGNORE INTO investimentos (nome, tipo, perfil_minimo, rentabilidade, vencimento_dias) VALUES (?, ?, ?, ?, ?)',
            investimentos
        )
        self.conn.commit()
    
    def criar_usuario(self, nome, email, senha, perfil='conservador'):
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        try:
            self.cursor.execute(
                'INSERT INTO usuarios (nome, email, senha_hash, perfil) VALUES (?, ?, ?, ?)',
                (nome, email, senha_hash, perfil)
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def verificar_login(self, email, senha):
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        self.cursor.execute(
            'SELECT id, nome, perfil FROM usuarios WHERE email = ? AND senha_hash = ?',
            (email, senha_hash)
        )
        return self.cursor.fetchone()
    
    def listar_investimentos(self, tipo=None):
        if tipo:
            self.cursor.execute('SELECT * FROM investimentos WHERE tipo = ?', (tipo,))
        else:
            self.cursor.execute('SELECT * FROM investimentos')
        return self.cursor.fetchall()
    
    def investir(self, usuario_id, investimento_id, valor):
        try:
            self.cursor.execute(
                'INSERT INTO user_investimentos (usuario_id, investimento_id, valor) VALUES (?, ?, ?)',
                (usuario_id, investimento_id, valor)
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def meus_investimentos(self, usuario_id):
        self.cursor.execute('''
            SELECT ui.*, i.nome, i.tipo, i.rentabilidade 
            FROM user_investimentos ui
            JOIN investimentos i ON ui.investimento_id = i.id
            WHERE ui.usuario_id = ?
        ''', (usuario_id,))
        return self.cursor.fetchall()