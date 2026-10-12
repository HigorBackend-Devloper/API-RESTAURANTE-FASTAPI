from pydantic import BaseModel
from typing import Optional


class Restaurantes_criar(BaseModel):
    nome: str
    categoria: str
    ativo: bool = False


class RestauranteAtualizacao(BaseModel):
    nome: str | None = None
    categoria: str | None = None
    ativo: bool | None = None


class Deletar_Restaurante(BaseModel):
    nome: str
    categoria: str
    ativo: bool


class Ativar_Restaurante(BaseModel):
    ativo: bool

class Desativar_Restaurante(BaseModel):
    ativo: bool
    
class RestauranteListagem(BaseModel):
    id: int
    nome: str
    categoria: str
    ativo: bool

class Restaurante_Parte_Atualizacao(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    ativo: Optional[bool] = None

