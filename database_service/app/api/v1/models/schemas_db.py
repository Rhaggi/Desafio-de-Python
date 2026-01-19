from pydantic import BaseModel
from typing import Optional

class ClienteSchema(BaseModel):
    nome: str
    email: str
    telefone: int
    correntista: bool = True
    saldo: Optional[float]

    class Config:
        from_attributes = True
