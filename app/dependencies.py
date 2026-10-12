from typing import Annotated

from app.database.database import Banco_de_dados
from app.repositories.restaurante_repository import RestauranteRepositorio
from app.repositories.usuario_repository import UsuarioRepositorio
from fastapi import Depends

banco_de_dados = Banco_de_dados()


def obter_banco_de_dados_local() -> Banco_de_dados:
    return banco_de_dados


def obter_usuario_repositorio(
    banco: Annotated[Banco_de_dados, Depends(obter_banco_de_dados_local)],
) -> UsuarioRepositorio:
    return UsuarioRepositorio(banco)


def obter_restaurantes_repositorio(
    banco: Annotated[Banco_de_dados, Depends(obter_banco_de_dados_local)],
) -> RestauranteRepositorio:
    return RestauranteRepositorio(banco)
