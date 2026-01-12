from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[4]
DB_PATH = BASE_DIR / 'db' / 'javer.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS clientes(
               id integer primary key autoincrement,
                nome TEXT NOT NULL,
               telefone INTEGER,
               correntista BOOLEAN NOT NULL DEFAULT 1,
               saldo_cc REAL
               )''')


conn.commit()
conn.close()
