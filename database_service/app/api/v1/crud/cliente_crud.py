import sqlite3

conn = sqlite3.connect('javer.db')
cursor = conn.cursor()


def criar(nome, email, telefone, correntista, saldo):
    cursor.execute('INSERT INTO clientes (nome, email, telefone, correntista, saldo_cc) VALUES (?, ?, ?, ?, ?)', (nome, email, telefone, correntista, saldo))
    conn.commit()
    print('Usuário criado com sucesso!')

def ler():
    for linha in cursor.execute('SELECT * FROM clientes'):
        print(linha)

def atualizar(id, nome):
    cursor.execute('UPDATE clientes SET nome = ? WHERE id = ?', (nome, id))
    conn.commit()
    print('Usuário atualizado com sucesso!')

def deletar(id):
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    print('Usuário deletado com sucesso!')

conn.commit()
conn.close()