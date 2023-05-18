from datetime import date
from typing import List  
from pydantic import BaseModel

class VendedorBase(BaseModel):
    nome: str
    senha: str
class VendedorCreate(VendedorBase):
    nome: str
    senha: str
    email: str
    comissao: int
    data_nascimento: date
    data_admissao: date
    cpf: str
    status: int
    id_endereco: int
    #email_ids: List[int] = []
    
class Vendedor(VendedorBase):
    id: int
    class Config:
        orm_mode = True
class PaginatedVendedor(BaseModel):
    limit: int
    offset: int
    data: List[Vendedor]

class VeiculoBase(BaseModel):
    nome: str
    status: int
    id_cor: int
    id_valor:int
    id_gasto: int

class VeiculoCreate(VeiculoBase):
    gasto_ids: List[int] = []
    pass

class Veiculo(VeiculoBase):
    id: int
    class Config:
        orm_mode = True

class PaginatedVeiculo(BaseModel):
    limit: int
    offset: int
    data: List[Veiculo]


class EnderecoBase(BaseModel):
    cep: str
    rua: str
    numero: int
    complemento: str
    bairro: str
    id_cidade:int

class EnderecoCreate(EnderecoBase):
    vendedore_ids: List[int] = []
    pass

class Endereco(EnderecoBase):
    id: int
    class Config:
        orm_mode = True

class PaginatedEndereco(BaseModel):
    limit: int
    offset: int
    data: List[Endereco]

class VendaBase(BaseModel):
    valor_venda: float
    forma_pagamento:int
    id_veiculo:int

class VendaUpdate(BaseModel):
    valor_venda: int

class VendaCreate(VendaBase):
    veiculo_ids: List[int] = []
    pass

class Venda(VendaBase):
    id: int
    veiculos: List[Veiculo] = []
    class Config:
        orm_mode = True

class PaginatedVenda(BaseModel):
    limit: int
    offset: int
    data: List[Venda]

class VendedorLoginSchema(BaseModel):
    email: str
    senha: str
    class Config:
        schema_extra = {
            "example": {
            "email": "x@x.com",
            "senha": "pass"
            }
        }
