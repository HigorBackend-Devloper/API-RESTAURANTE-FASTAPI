from typing import Annotated

from app.routers.usuarios import dados_pagina_login
from app.templates import templates
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/registro", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request, "registro.html")


@router.get("/login", response_class=HTMLResponse)
async def pagina_login(
    request: Request,
    dados: Annotated[dict, Depends(dados_pagina_login)],
):
    return templates.TemplateResponse(request, "login.html", dados)
