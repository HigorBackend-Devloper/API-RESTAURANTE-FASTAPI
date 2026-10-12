import hashlib
import hmac
import secrets

# A senha nunca é gravada: só o hash. Formato salvo no banco: "salt$hash" (em hexadecimal).


def gerar_hash_senha(senha: str) -> str:
    salt = secrets.token_bytes(16)
    hash_ = hashlib.scrypt(senha.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"{salt.hex()}${hash_.hex()}"


def verificar_senha(senha: str, senha_hash: str) -> bool:
    salt_hex, hash_hex = senha_hash.split("$")
    hash_ = hashlib.scrypt(
        senha.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1
    )
    return hmac.compare_digest(hash_.hex(), hash_hex)
