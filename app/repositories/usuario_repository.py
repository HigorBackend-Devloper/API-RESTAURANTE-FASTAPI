from app.database.database import Banco_de_dados


class UsuarioRepositorio:
    def __init__(self, database: Banco_de_dados):
        self.db = database

    async def registro_usuario(self, nome: str, email: str, senha: str) -> int | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO usuarios(nome,email,senha) VALUES (?,?,?)",
                (nome, email, senha),
            )

            return cursor.lastrowid

    async def obter_usuario(self, usuario_id: int) -> dict | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email FROM usuarios WHERE id = ?",
                (usuario_id,),
            )
            linha = cursor.fetchone()
            if linha:
                return {"id_": linha[0], "nome": linha[1], "email": linha[2]}
            return None

    async def obter_usuario_por_email(self, email: str) -> tuple | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,)
            )
            linha = cursor.fetchone()
            return linha
