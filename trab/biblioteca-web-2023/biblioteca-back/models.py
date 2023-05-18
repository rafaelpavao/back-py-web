from sqlalchemy import Column, Integer, String, SmallInteger, Date, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from database import Base

class Cor(Base):
    __tablename__ = 'cor'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))

    veiculos = relationship('Veiculo', back_populates='cor')

class Veiculo(Base):
    __tablename__ = 'veiculo'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    status = Column(SmallInteger)

    id_cor = Column(Integer, ForeignKey('cor.id'), nullable=False)
    cor = relationship('Cor', back_populates='veiculos')

    id_valor = Column(Integer, ForeignKey('valor.id'), nullable=False)
    valor = relationship('Valor', back_populates='veiculos')

    id_modelo = Column(Integer, ForeignKey('modelo.id'), nullable=False)
    modelo = relationship('Modelo', back_populates='veiculos')
    
    gastos = relationship('Gasto', back_populates='veiculo')
    vendas = relationship('Venda', back_populates='veiculo')

class Venda(Base):
    __tablename__ = 'venda'
    
    id = Column(Integer, primary_key=True, index=True)
    valor_venda = Column(Float)
    forma_pagamento = Column(Integer)

    id_veiculo = Column(Integer, ForeignKey('veiculo.id'), nullable=False)
    veiculo = relationship('Veiculo', back_populates='vendas')

class Gasto(Base):
    __tablename__ = 'gasto'
    
    id = Column(Integer, primary_key=True, index=True)
    valor_gasto = Column(Float)
    descricao = Column(String(255))

    id_veiculo = Column(Integer, ForeignKey('veiculo.id'), nullable=False)
    veiculo = relationship('Veiculo', back_populates='gastos')


class Modelo(Base):
    __tablename__ = 'modelo'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    litragem_motor = Column(Float(2))
    ano_fab = Column(Integer)
    ano_modelo = Column(Integer)
    cambio = Column(Integer)
    num_portas = Column(Integer)
    capacidade = Column(Integer)
    combustivel = Column(Integer)
    carroceria = Column(Integer)

    id_marca = Column(Integer, ForeignKey('marca.id'), nullable=False)

    veiculos = relationship('Veiculo', back_populates='modelo')
    marca = relationship('Marca', back_populates='modelos')

class Marca(Base):
    __tablename__ = 'marca'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50))

    modelos = relationship('Modelo', back_populates='marca')


class Valor(Base):
    __tablename__ = 'valor'
    
    id = Column(Integer, primary_key=True, index=True)
    valor_pago = Column(Float)
    valor_fipe = Column(Float)
    valor_venda = Column(Float)

    veiculos = relationship('Veiculo', back_populates='valor')


class Vendedor(Base):
    __tablename__ = 'vendedor'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    senha = Column(String(255))
    email = Column(String(150), unique=True, index=True)
    comissao = Column(Integer)
    data_nascimento = Column(Date)
    data_admissao = Column(Date)
    cpf = Column(String(14))
    status = Column(SmallInteger)

    id_endereco = Column(Integer, ForeignKey('endereco.id'), nullable=False)
    endereco = relationship('Endereco', back_populates='vendedores')

class Endereco(Base):
    __tablename__ = 'endereco'
    
    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String(8))
    rua = Column(String(100))
    numero = Column(SmallInteger)
    complemento = Column(String(100))
    bairro = Column(String(100))

    id_cidade = Column(Integer, ForeignKey('cidade.id'), nullable=False)
    cidade = relationship('Cidade', back_populates='enderecos')

    vendedores = relationship('Vendedor', back_populates='endereco')

class Cidade(Base):
    __tablename__ = 'cidade'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))

    id_estado = Column(Integer, ForeignKey('estado.id'), nullable=False)
    estado = relationship('Estado', back_populates='cidades')

    enderecos = relationship('Endereco', back_populates='cidade')

class Estado(Base):
    __tablename__ = 'estado'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    sigla = Column(String(2))

    cidades = relationship('Cidade', back_populates='estado')