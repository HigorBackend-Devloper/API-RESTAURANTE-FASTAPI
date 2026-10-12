from app.database.database import Banco_de_dados
from app.schemas import restaurante


class RestauranteRepositorio:
    def __init__(self, database: Banco_de_dados):
        self.db = database

    async def registro_restaurante(
        self, nome: str, categoria: str, ativo: bool
    ) -> int | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, ?)",
                (nome, categoria, ativo),
            )
            return cursor.lastrowid

    async def obter_restaurantes(self):
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, categoria, ativo FROM restaurantes")
            return cursor.fetchall()

    async def obter_restaurante_id(self, restaurante_id: int):
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, categoria, ativo FROM restaurantes WHERE id = ?",
                (restaurante_id,),
            )
            return cursor.fetchone()

    async def editar_restaurantes_id(
        self,
        restaurante_id: int,
        dados: restaurante.RestauranteAtualizacao,
    ) -> restaurante:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE restaurantes SET nome = ?, categoria = ?, ativo = ? WHERE id = ?",
                (dados.nome, dados.categoria, dados.ativo, restaurante_id),
            )
            return cursor.rowcount > 0

    async def deletar_restaurante(self, restaurante_id: int):
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM restaurantes WHERE id = ?",
                (restaurante_id,),
            )
            return cursor.rowcount > 0

    async def ativar_restaurante_id(self, restaurante_id: int):
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE restaurantes SET ativo = 1 WHERE id = ?",
                (restaurante_id,),
            )
            return cursor.rowcount > 0

    async def desativar_restaurante_id(self, restaurante_id: int):
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE restaurantes SET ativo = 0 WHERE id = ?",
                (restaurante_id,),
            )
            return cursor.rowcount > 0
