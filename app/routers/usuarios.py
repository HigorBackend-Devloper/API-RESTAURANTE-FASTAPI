from typing import Annotated
from urllib.parse import urlencode

from app.dependencies import obter_usuario_repositorio
from app.repositories.usuario_repository import UsuarioRepositorio
from app.schemas.usuario import usuario_login, usuario_registro
from app.services.auth_service import gerar_hash_senha, verificar_senha
from app.templates import templates
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()


@router.post("/registro", response_class=HTMLResponse)
async def cadastrar_usuario(
    request: Request,
    dados: Annotated[usuario_registro, Form()],
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)
    ],
):
    # Já tem conta: manda para o login com o email preenchido
    if await usuario_repositorio.obter_usuario_por_email(dados.email):
        query = urlencode({"email": dados.email, "aviso": "conta_existente"})
        return RedirectResponse(f"/login?{query}", status_code=303)

    if dados.senha != dados.confirmar_senha:
        return templates.TemplateResponse(
            request,
            "registro.html",
            {
                "erro": "As senhas não conferem",
                "nome": dados.nome,
                "email": dados.email,
            },
        )

    await usuario_repositorio.registro_usuario(
        dados.nome, dados.email, gerar_hash_senha(dados.senha)
    )
    return RedirectResponse("/login", status_code=303)


@router.get("/me")
async def me(
    request: Request,
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)
    ],
):
    usuario_id = request.cookies.get("session_token")

    if not usuario_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    usuario = await usuario_repositorio.obter_usuario(int(usuario_id))

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


@router.post("/login", response_class=HTMLResponse)
async def login_usuario(
    request: Request,
    dados: Annotated[usuario_login, Form()],
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)
    ],
):
    usuario_encontrado = await usuario_repositorio.obter_usuario_por_email(dados.email)

    if usuario_encontrado is None or not verificar_senha(
        dados.senha, usuario_encontrado[3]
    ):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"erro": "E-mail ou senha inválidos", "email": dados.email},
        )

    response = RedirectResponse("/", status_code=303)

    # A página inicial usa este cookie para buscar o usuário.
    response.set_cookie(
        key="session_token",
        value=str(usuario_encontrado[0]),
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return response


@router.get("/logout")
@router.post("/logout")
async def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("session_token")
    return response


def dados_pagina_login(request: Request):
    erro = None
    if request.query_params.get("aviso") == "conta_existente":
        erro = "Já existe uma conta com este e-mail. Entre com sua senha."

    return {"email": request.query_params.get("email", ""), "erro": erro}
