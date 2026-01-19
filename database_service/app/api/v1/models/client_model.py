from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path("C:/Users/RosalinaTeixeiraOliv/Documents/Cursos/Desafio de Python")
DB_PATH = BASE_DIR / 'db' / 'javer.db'
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

db = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

sessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=db)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    telefone = Column(Integer, index=True)
    correntista = Column(Boolean, default=True)
    saldo = Column('saldo_cc', Float, default=0.0)

    def __init__(self, nome: str,  email: str, telefone: int, correntista: bool = False, saldo: float = 0.0):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.correntista = correntista
        self.saldo = saldo
Base.metadata.create_all(bind=db)
