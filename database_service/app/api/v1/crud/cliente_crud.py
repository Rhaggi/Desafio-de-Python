import sqlite3

conn = sqlite3.connect('javer.db')
cursor = conn.cursor()


def criar(nome):
    cursor.execute('INSERT INTO clientes (nome) VALUES (?)', (nome,))
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