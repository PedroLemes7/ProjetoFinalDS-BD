import mysql.connector
import traceback
from db_config import db_config

class Cadastro:
    def __init__(self, nome, email, senha, telefone, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone

    @staticmethod
    def _get_connection():
        return mysql.connector.connect(**db_config)

    def salvar(self):
        """Salva um cadastro no banco. Se o ID existir, atualiza. Senão, cria um novo."""
        conn = Cadastro._get_connection()
        try:
            cursor = conn.cursor()
            if self.id:
                query = "UPDATE cadastro SET nome = %s, email = %s, senha = %s, telefone = %s WHERE id = %s"
                cursor.execute(query, (self.nome, self.email, self.senha, self.telefone, self.id))
            else:
                query = "INSERT INTO cadastro (nome, email, senha, telefone) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (self.nome, self.email, self.senha, self.telefone))
                self.id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as erro:
            if conn.is_connected():
                conn.rollback()
            
            print ("codigo do erro {erro.errno}")
            print ("mensagem do erro {erro.msg}")

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