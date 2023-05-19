from datetime import date
from sqlalchemy.orm import Session
from exceptions import VeiculoAlreadyExistError, VeiculoNotFoundError, VeiculoNotFoundError, VendaNotFoundError, VendedorNotFoundError, VendedorAlreadyExistError, EnderecoNotFoundError
import models, schemas, bcrypt

# endereco
def create_endereco(db: Session, endereco: schemas.EnderecoCreate):
    db_endereco = models.Endereco(**endereco.dict())
    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)
    return db_endereco

def delete_endereco_by_id(db: Session, endereco_id: int):
    db_endereco = get_endereco_by_id(db, endereco_id)
    db.delete(db_endereco)
    db.commit()
    return

def get_endereco_by_id(db: Session, endereco_id: int):
    db_endereco = db.query(models.Endereco).get(endereco_id)
    if db_endereco is None:
        raise EnderecoNotFoundError
    return db_endereco

# vendedor
def get_vendedor_by_id(db: Session, vendedor_id: int):
    db_vendedor = db.query(models.Vendedor).get(vendedor_id)
    if db_vendedor is None:
        raise VendedorNotFoundError
    return db_vendedor

def get_all_vendedores(db: Session, offset: int, limit: int):
    return db.query(models.Vendedor).offset(offset).limit(limit).all()

def get_vendedor_by_email(db: Session, vendedor_email: str):
    return db.query(models.Vendedor).filter(models.Vendedor.email == vendedor_email).first()

def create_vendedor(db: Session, vendedor: schemas.VendedorCreate):
    db_vendedor = get_vendedor_by_email(db, vendedor.email)
    # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
    vendedor.senha = bcrypt.hashpw(vendedor.senha.encode('utf8'), bcrypt.gensalt())
    if db_vendedor is not None:
        raise VendedorAlreadyExistError
    db_vendedor = models.Vendedor(**vendedor.dict())
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def update_vendedor(db: Session, vendedor_id: int, vendedor: schemas.VendedorCreate):
    db_vendedor = get_vendedor_by_id(db, vendedor_id)
    db_vendedor.nome = vendedor.nome
    db_vendedor.email = vendedor.email
    db_vendedor.senha = vendedor.senha
    db_vendedor.comissao = vendedor.comissao
    db_vendedor.data_nascimento = vendedor.data_nascimento
    db_vendedor.data_admissao = vendedor.data_admissao
    db_vendedor.cpf = vendedor.cpf
    db_vendedor.status = vendedor.status
    db_vendedor.id_endereco = vendedor.id_endereco
    if vendedor.senha != "":
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        db_vendedor.senha = bcrypt.hashpw(vendedor.senha.encode('utf8'), bcrypt.gensalt())
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def delete_vendedor_by_id(db: Session, vendedor_id: int):
    db_vendedor = get_vendedor_by_id(db, vendedor_id)
    db.delete(db_vendedor)
    db.commit()
    return

# veiculo
def get_veiculo_by_id(db: Session, veiculo_id: int):
    db_veiculo = db.query(models.Veiculo).get(veiculo_id)
    if db_veiculo is None:
        raise VeiculoNotFoundError
    return db_veiculo

def get_all_veiculos(db: Session, offset: int, limit: int):
    return db.query(models.Veiculo).offset(offset).limit(limit).all()

def create_veiculo(db: Session, veiculo: schemas.VeiculoCreate):
    db_veiculo = models.Veiculo(**veiculo.dict())
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo

def update_veiculo(db: Session, veiculo_id: int, veiculo: schemas.VeiculoCreate):
    db_veiculo = get_veiculo_by_id(db, veiculo_id)

    db_veiculo.nome = veiculo.nome
    db_veiculo.status = veiculo.status

    db_veiculo.id_cor = veiculo.id_cor
    db_veiculo.id_valor = veiculo.id_valor
    #db_veiculo.id_gasto = veiculo.id_gasto

    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo

def delete_veiculo_by_id(db: Session, veiculo_id: int):
    db_veiculo = get_veiculo_by_id(db, veiculo_id)
    db.delete(db_veiculo)
    db.commit()
    return

# venda
def create_venda(db: Session, venda: schemas.VendaCreate):
    db_venda = models.Venda(valor_venda=venda.valor_venda, forma_pagamento=venda.forma_pagamento)
    if (veiculos := db.query(models.Veiculo).filter(models.Veiculo.id.in_(venda.veiculo_ids))).count() == len(venda.veiculo_ids):
        db_venda.vendas.extend(veiculos)
    else:
        raise VendaNotFoundError

    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda

def get_venda_by_id(db: Session, venda_id: int):
    db_venda = db.query(models.Venda).get(venda_id)
    if db_venda is None:
        raise VendaNotFoundError
    return db_venda

def get_all_vendas(db: Session, offset: int, limit: int):
    return db.query(models.Venda).offset(offset).limit(limit).all()

def update_venda(db: Session, venda_id: int, venda: schemas.VendaUpdate):
    db_venda = get_venda_by_id(db, venda_id)
    db_venda.status = venda.status
    db.commit()
    db.refresh(db_venda)
    return db_venda

def check_vendedor(db: Session, vendedor: schemas.VendedorLoginSchema):
    db_vendedor = db.query(models.Vendedor).filter(models.Vendedor.email == vendedor.email).first()
    if db_vendedor is None:
        return False
    return bcrypt.checkpw(vendedor.senha.encode('utf8'), db_vendedor.senha.encode('utf8'))






