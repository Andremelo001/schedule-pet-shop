from passlib.context import CryptContext

class PasswordHasher():
    def __init__(self):
        self.crypt_context = CryptContext(schemes=['sha256_crypt'])

    def hash(self, senha: str) -> str:
        return self.crypt_context.hash(senha)
    

    def verify(self, senha: str, hash_senha: str) -> bool:
        return self.crypt_context.verify(senha, hash_senha)
    
