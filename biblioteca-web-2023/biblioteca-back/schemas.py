from datetime import date
from typing import List  
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str
    email: str
class UsuarioCreate(UsuarioBase):
    senha: str
class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True
class PaginatedUsuario(BaseModel):
    limit: int
    offset: int
    data: List[Usuario]

class LivroBase(BaseModel):
    titulo: str
    resumo: str
class LivroCreate(LivroBase):
    pass
class Livro(LivroBase):
    id: int
    class Config:
        orm_mode = True
class PaginatedLivro(BaseModel):
    limit: int
    offset: int
    data: List[Livro]

class EmprestimoBase(BaseModel):
    id_usuario: int
    status: int
    data_retirada: date
class EmprestimoUpdate(BaseModel):
    status: int
class EmprestimoCreate(EmprestimoBase):
    livro_ids: List[int] = []
    pass
class Emprestimo(EmprestimoBase):
    id: int
    usuario: Usuario = {}
    livros: List[Livro] = []
    class Config:
        orm_mode = True
class PaginatedEmprestimo(BaseModel):
    limit: int
    offset: int
    data: List[Emprestimo]

class UsuarioLoginSchema(BaseModel):
    email: str
    senha: str
    class Config:
        schema_extra = {
            "example": {
            "email": "x@x.com",
            "senha": "pass"
            }
        }
