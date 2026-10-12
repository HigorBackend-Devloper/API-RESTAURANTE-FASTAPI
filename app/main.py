from app.routers import (
    frontend,
    frontend_restaurantes,
    frontend_usuarios,
    restaurantes,
    usuarios,
)
from app.templates import BASE_DIR, templates
from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Restaurante-Higor", description="API do Restaurante-Higor", version="1.0.0"
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.exception_handler(RequestValidationError)
async def erro_validacao_formulario(request: Request, exc: RequestValidationError):
    if request.method != "POST":
        return await request_validation_exception_handler(request, exc)

    if request.url.path == "/login":
        pagina = "login.html"
    elif request.url.path == "/registro":
        pagina = "registro.html"
    else:
        return await request_validation_exception_handler(request, exc)

    dados = await request.form()
    return templates.TemplateResponse(
        request,
        pagina,
        {
            "erro": "Preencha todos os campos corretamente.",
            "nome": dados.get("nome", ""),
            "email": dados.get("email", ""),
        },
        status_code=422,
    )


@app.get("/health")
async def health_check():
    return {"status": "API is running"}


app.include_router(usuarios.router)
app.include_router(frontend.router)
app.include_router(restaurantes.router)

app.include_router(frontend_usuarios.router)
app.include_router(frontend_restaurantes.router)
