from flask import Flask, render_template, request, redirect, url_for
from model import Cadastro

app = Flask(__name__)

# Rota principal (Read - Listar todos)
@app.route('/', methods=['GET','POST'])
def index():
    cadastro = Cadastro.buscar_todos()
    return render_template('cadastro.html', cadastro=cadastro)

# Rota para exibir o formulário de novo cadastro
@app.route('/novo', methods=['POST', 'GET'])
def novo():
    return render_template('cadastro.html', cadastro=None)

# Rota para salvar um novo cadastro (Create)
@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']
    cadastro =  Cadastro(nome=nome, email=email, senha=senha, telefone=telefone)
    cadastro.salvar()
    """  return redirect(url_for('index')) """
    return cadastro


# Rota para exibir o formulário de edição (preenche com dados)
@app.route('/editar/<int:id>')
def editar(id):
    cadastro = Cadastro.buscar_por_id(id)
    return render_template('cadastro.html', cadastro=cadastro)

# Rota para atualizar um cadastro existente (Update)
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']
    cadastro = Cadastro(id=id, nome=nome, email=email, senha=senha,telefone=telefone)
    cadastro.salvar() # O método salvar já lida com a atualização se o ID existir
    return redirect(url_for('index'))

# Rota para deletar um cadastro (Delete)
@app.route('/deletar/<int:id>')
def deletar(id):
    Cadastro.deletar(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)