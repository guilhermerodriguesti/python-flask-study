# Importar bibliotecas
from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('study.db')
c = conn.cursor()

# Criar tabela se ela não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS estudo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        materia TEXT NOT NULL,
        topico TEXT NOT NULL,
        duracao INTEGER NOT NULL,
        objetivo TEXT NOT NULL,
        notas TEXT,
        recursos TEXT,
        compreensao INTEGER NOT NULL,
        revisao TEXT NOT NULL
    )
''')

# Fechar conexão com o banco de dados
conn.close()

# Inicializar aplicação Flask
app = Flask(__name__)

# Rota principal
@app.route('/')
def index():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    
    # Obter todos os registros do banco de dados
    c.execute('SELECT * FROM estudo')
    registros = c.fetchall()
    
    # Fechar conexão com o banco de dados
    conn.close()
    
    # Renderizar template com os registros
    return render_template('index.html', registros=registros)

# Rota para adicionar um registro de estudo
@app.route('/estudar', methods=['GET', 'POST'])
def estudar():
    if request.method == 'POST':
        # Obter os dados do formulário
        data = request.form['data']
        materia = request.form['materia']
        topico = request.form['topico']
        duracao = request.form['duracao']
        objetivo = request.form['objetivo']
        notas = request.form['notas']
        recursos = request.form['recursos']
        compreensao = request.form['compreensao']
        revisao = request.form['revisao']
        
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('study.db')
        c = conn.cursor()
        
        # Inserir o registro no banco de dados
        c.execute('''
            INSERT INTO estudo (data, materia, topico, duracao, objetivo, notas, recursos, compreensao, revisao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data, materia, topico, duracao, objetivo, notas, recursos, compreensao, revisao))
        
        # Salvar as alterações no banco de dados
        conn.commit()
        
        # Fechar conexão com o banco de dados
        conn.close()
        
        # Redirecionar para a página principal
        return redirect('/')
    
    # Renderizar o formulário para adicionar um registro
    return render_template('estudar.html')

# Rota para atualizar um registro de estudo
@app.route('/revisar-conteudo/<int:id>', methods=['GET', 'POST'])
def revisar_conteudo(id):
    if request.method == 'POST':
        # Obter os dados do formulário
        compreensao = request.form['compreensao']
        revisao = request.form['revisao']
        
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('study.db')
        c = conn.cursor()
        
        # Atualizar o registro no banco de dados
        c.execute('''
            UPDATE estudo
            SET compreensao = ?, revisao = ?
            WHERE id = ?
        ''', (compreensao, revisao, id))
        
        # Salvar as alterações no banco de dados
        conn.commit()
        
        # Fechar conexão com o banco de dados
        conn.close()
        
        # Redirecionar para a página principal
        return redirect('/')
    
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    
    # Obter o registro com base no ID fornecido
    c.execute('SELECT * FROM estudo WHERE id = ?', (id,))
    registro = c.fetchone()
    
    # Fechar conexão com o banco de dados
    conn.close()
    
    # Renderizar o formulário para atualizar o registro
    return render_template('revisar-conteudo.html', registro=registro)


# Rota para revisar o conteúdo com base no Nível de Compreensão e na revisão espaçada
@app.route('/revisar-materia')
def revisar_materia():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('study.db')
    c = conn.cursor()

    # Obter os registros para revisão com base no Nível de Compreensão e na revisão espaçada
    c.execute('SELECT * FROM estudo WHERE compreensao < 7 AND revisao = 1')
    registros = c.fetchall()

    # Fechar conexão com o banco de dados
    conn.close()

    # Renderizar o template para revisar os registros
    return render_template('revisar-materia.html', registros=registros)

# Rota para atualizar a revisão de conteúdo com base no Nível de Compreensão e na revisão espaçada
@app.route('/atualizar-revisao', methods=['POST'])
def atualizar_revisao():
    # Obter os registros para revisão com base no Nível de Compreensão e na revisão espaçada
    registros = request.form.getlist('registro')

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('study.db')
    c = conn.cursor()

    for registro_id in registros:
        # Atualizar a revisão para 0 (revisado)
        c.execute('UPDATE estudo SET revisao = 0 WHERE id = ?', (registro_id,))

    # Salvar as alterações no banco de dados
    conn.commit()

    # Fechar conexão com o banco de dados
    conn.close()

    # Redirecionar para a página de revisão
    return redirect('/revisar-materia')


app.run(host='0.0.0.0', port=8000)



