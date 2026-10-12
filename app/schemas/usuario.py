from pydantic import BaseModel


class usuario_registro(BaseModel):
    nome: str
    email: str
    senha: str
    confirmar_senha: str


class usuario_login(BaseModel):
    email: str
    senha: str
