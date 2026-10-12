from typing import Annotated

from app.dependencies import obter_usuario_repositorio
from app.repositories.usuario_repository import UsuarioRepositorio
from app.routers.restaurantes import listar_restaurantes
from app.schemas.restaurante import RestauranteListagem
from app.templates import templates
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def pagina_inicial(
    request: Request,
    repositorio: Annotated[UsuarioRepositorio, Depends(obter_usuario_repositorio)],
    restaurantes: Annotated[list[RestauranteListagem], Depends(listar_restaurantes)],
):
    usuario = None
    token = request.cookies.get("session_token")
    try:
        usuario_id = int(token) if token else None
    except ValueError:
        usuario_id = None
    if usuario_id is not None and 0 < usuario_id <= 9223372036854775807:
        usuario = await repositorio.obter_usuario(usuario_id)

    total_ativos = sum(1 for r in restaurantes if r.ativo)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "usuario": usuario,
            "restaurantes": restaurantes,
            "total_restaurantes": len(restaurantes),
            "total_ativos": total_ativos,
            "total_inativos": len(restaurantes) - total_ativos,
        },
    )
