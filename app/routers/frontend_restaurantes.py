from typing import Annotated

from app.routers.restaurantes import listar_restaurantes, pegar_restaurante_id
from app.schemas.restaurante import RestauranteListagem
from app.templates import templates
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/restaurantes", response_class=HTMLResponse)
async def pagina_restaurantes(
    request: Request,
    restaurantes: Annotated[list[RestauranteListagem], Depends(listar_restaurantes)],
):
    return templates.TemplateResponse(
        request, "restaurantes.html", {"restaurantes": restaurantes}
    )


@router.get("/restaurantes/novo", response_class=HTMLResponse)
async def pagina_novo_restaurante(request: Request):
    return templates.TemplateResponse(request, "restaurante-form.html")


@router.get("/restaurantes/{restaurante_id}/editar", response_class=HTMLResponse)
async def pagina_editar_restaurante(
    request: Request,
    restaurante: Annotated[RestauranteListagem, Depends(pegar_restaurante_id)],
):
    return templates.TemplateResponse(
        request, "restaurante-form.html", {"restaurante": restaurante}
    )


@router.get("/restaurantes/{restaurante_id}", response_class=HTMLResponse)
async def pagina_restaurante(
    request: Request,
    restaurante: Annotated[RestauranteListagem, Depends(pegar_restaurante_id)],
):
    return templates.TemplateResponse(
        request, "restaurante-detalhes.html", {"restaurante": restaurante}
    )
