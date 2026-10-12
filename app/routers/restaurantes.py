from typing import Annotated

from app.dependencies import obter_restaurantes_repositorio
from app.repositories.restaurante_repository import RestauranteRepositorio
from app.schemas.restaurante import (
    RestauranteListagem,
    Restaurantes_criar,
    RestauranteAtualizacao,
    Restaurante_Parte_Atualizacao,
    Ativar_Restaurante,
    Desativar_Restaurante,
)
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.post("/restaurantes")
async def criar_restaurante(
    dados: Annotated[Restaurantes_criar, Form()],
    restaurante_repositorio: Annotated[
        RestauranteRepositorio,
        Depends(obter_restaurantes_repositorio),
    ],
):
    await restaurante_repositorio.registro_restaurante(
        dados.nome, dados.categoria, dados.ativo
    )
    return RedirectResponse("/restaurantes", status_code=303)


async def listar_restaurantes(
    restaurante_repositorio: Annotated[
        RestauranteRepositorio, Depends(obter_restaurantes_repositorio)
    ],
):
    linhas = await restaurante_repositorio.obter_restaurantes()
    restaurantes = []

    for linha in linhas:
        restaurante = RestauranteListagem(
            id=linha[0],
            nome=linha[1],
            categoria=linha[2],
            ativo=linha[3],
        )
        restaurantes.append(restaurante)

    return restaurantes


@router.get("/restaurante/{restaurante_id}")
async def pegar_restaurante_id(
    restaurante_id: int,
    restaurante_repositorio: Annotated[
        RestauranteRepositorio,
        Depends(obter_restaurantes_repositorio),
    ],
):
    linha = await restaurante_repositorio.obter_restaurante_id(restaurante_id)
    if linha is None:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")

    restaurante = RestauranteListagem(
        id=linha[0],
        nome=linha[1],
        categoria=linha[2],
        ativo=linha[3],
    )
    return restaurante


@router.post("/restaurantes/{restaurante_id}/editar")
async def salvar_edicao_restaurante(
    restaurante_id: int,
    dados: Annotated[RestauranteAtualizacao, Form()],
    restaurante_repositorio: Annotated[
        RestauranteRepositorio, Depends(obter_restaurantes_repositorio)
    ],
):
    await atualizar_restaurante(restaurante_id, dados, restaurante_repositorio)
    return RedirectResponse(f"/restaurantes/{restaurante_id}", status_code=303)


@router.put("/restaurante", response_model=RestauranteListagem)
async def atualizar_restaurante(
    restaurante_id: int,
    dados: RestauranteAtualizacao,
    restaurante_repositorio: Annotated[
        RestauranteRepositorio,
        Depends(obter_restaurantes_repositorio),
    ],
):
    if dados.nome is None or dados.categoria is None or dados.ativo is None:
        raise HTTPException(status_code=422, detail="Informe nome, categoria e ativo")

    atualizado = await restaurante_repositorio.editar_restaurantes_id(
        restaurante_id, dados
    )

    if not atualizado:
        raise HTTPException(status_code=422, detail="Informe nome, categoria e ativo")
    return RestauranteListagem(
        id=restaurante_id,
        nome=dados.nome,
        categoria=dados.categoria,
        ativo=dados.ativo,
    )


@router.patch("/restaurante/{restaurante_id}", response_model=RestauranteListagem)
async def atualizar_parte_restaurante(
    restaurante_id: int,
    dados: Restaurante_Parte_Atualizacao,
    restaurante_repositorio: Annotated[
        RestauranteRepositorio, Depends(obter_restaurantes_repositorio)
    ],
):
    linha = await restaurante_repositorio.obter_restaurante_id(restaurante_id)
    if linha is None:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")

    atual = RestauranteListagem(
        id=linha[0], nome=linha[1], categoria=linha[2], ativo=linha[3]
    )

    # só os campos que o cliente realmente enviou
    alteracoes = dados.model_dump(exclude_unset=True)
    if not alteracoes:
        raise HTTPException(status_code=422, detail="Informe ao menos um campo")

    restaurante_atualizado = atual.model_copy(update=alteracoes)

    await restaurante_repositorio.editar_restaurantes_id(
        restaurante_id, restaurante_atualizado
    )
    return restaurante_atualizado


@router.post("/restaurantes/{restaurante_id}/status")
async def alterar_status_restaurante(
    restaurante_id: int,
    ativo: Annotated[bool, Form()],
    restaurante_repositorio: Annotated[
        RestauranteRepositorio, Depends(obter_restaurantes_repositorio)
    ],
):
    encontrado = await restaurante_repositorio.obter_restaurante_id(restaurante_id)
    if encontrado is None:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")

    if ativo:
        await restaurante_repositorio.ativar_restaurante_id(restaurante_id)
    else:
        await restaurante_repositorio.desativar_restaurante_id(restaurante_id)

    return RedirectResponse(f"/restaurantes/{restaurante_id}", status_code=303)


@router.post("/restaurantes/{restaurante_id}/excluir")
async def excluir_restaurante_form(
    restaurante_id: int,
    restaurante_repositorio: Annotated[
        RestauranteRepositorio, Depends(obter_restaurantes_repositorio)
    ],
):
    await restaurante_repositorio.deletar_restaurante(restaurante_id)
    return RedirectResponse("/restaurantes", status_code=303)
