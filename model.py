import mysql.connector
from db_config import db_config

class Cadastro:
    def __init__(self, nome, descricao, preco, id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    @staticmethod
    def _get_connection():
        return mysql.connector.connect(**db_config)

    def salvar(self):
        """Salva um cadastro no banco. Se o ID existir, atualiza. Senão, cria um novo."""
        conn = Cadastro._get_connection()
        cursor = conn.cursor()
        if self.id:
            query = "UPDATE cadastro SET nome = %s, descricao = %s, preco = %s WHERE id = %s"
            cursor.execute(query, (self.nome, self.descricao, self.preco, self.id))
        else:
            query = "INSERT INTO cadastro (nome, descricao, preco) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.nome, self.descricao, self.preco))
            self.id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar_todos():
        """Retorna uma lista de todos os cadastro do banco."""
        conn = Cadastro._get_connection()
        cursor = conn.cursor(dictionary=True) 
        query = "SELECT * FROM cadastro"
        cursor.execute(query)
        cadastro = cursor.fetchall()
        cursor.close()
        conn.close()
        return cadastro

    @staticmethod
    def buscar_por_id(id):
        """Busca um cadastro específico pelo seu ID."""
        conn = Cadastro._get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM cadastro WHERE id = %s"
        cursor.execute(query, (id,))
        cadastro = cursor.fetchone()
        cursor.close()
        conn.close()
        return cadastro

    @staticmethod
    def deletar(id):
        """Deleta um cadastro do banco de dados pelo seu ID."""
        conn = Cadastro._get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM cadastro WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        conn.close()