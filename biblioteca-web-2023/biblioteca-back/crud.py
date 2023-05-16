from sqlalchemy.orm import Session
from exceptions import UsuarioAlreadyExistError, UsuarioNotFoundError, LivroNotFoundError, EmprestimoNotFoundError
import bcrypt, models, schemas

# usuário
def get_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).get(usuario_id)
    if db_usuario is None:
        raise UsuarioNotFoundError
    return db_usuario

def get_all_usuarios(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).offset(offset).limit(limit).all()

def get_usuario_by_email(db: Session, usuario_email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == usuario_email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_email(db, usuario.email)
    # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
    usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt())
    if db_usuario is not None:
        raise UsuarioAlreadyExistError
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db_usuario.nome = usuario.nome
    db_usuario.email = usuario.email
    if usuario.senha != "":
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        db_usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt())
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db.delete(db_usuario)
    db.commit()
    return

# livro
def get_livro_by_id(db: Session, livro_id: int):
    db_livro = db.query(models.Livro).get(livro_id)
    if db_livro is None:
        raise LivroNotFoundError
    return db_livro

def get_all_livros(db: Session, offset: int, limit: int):
    return db.query(models.Livro).offset(offset).limit(limit).all()

def create_livro(db: Session, livro: schemas.LivroCreate):
    db_livro = models.Livro(**livro.dict())
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

def update_livro(db: Session, livro_id: int, livro: schemas.LivroCreate):
    db_livro = get_livro_by_id(db, livro_id)
    db_livro.titulo = livro.titulo
    db_livro.resumo = livro.resumo
    db.commit()
    db.refresh(db_livro)
    return db_livro

def delete_livro_by_id(db: Session, livro_id: int):
    db_livro = get_livro_by_id(db, livro_id)
    db.delete(db_livro)
    db.commit()
    return

# empréstimo
def create_emprestimo(db: Session, emprestimo: schemas.EmprestimoCreate):
    get_usuario_by_id(db, emprestimo.id_usuario)
    db_emprestimo = models.Emprestimo(id_usuario=emprestimo.id_usuario, status=emprestimo.status, data_retirada=emprestimo.data_retirada)
    if (livros := db.query(models.Livro).filter(models.Livro.id.in_(emprestimo.livro_ids))).count() == len(emprestimo.livro_ids):
        db_emprestimo.livros.extend(livros)
    else:
        raise LivroNotFoundError

    db.add(db_emprestimo)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo

def get_emprestimo_by_id(db: Session, emprestimo_id: int):
    db_emprestimo = db.query(models.Emprestimo).get(emprestimo_id)
    if db_emprestimo is None:
        raise EmprestimoNotFoundError
    return db_emprestimo

def get_all_emprestimos(db: Session, offset: int, limit: int):
    return db.query(models.Emprestimo).offset(offset).limit(limit).all()

def update_emprestimo(db: Session, emprestimo_id: int, emprestimo: schemas.EmprestimoUpdate):
    db_emprestimo = get_emprestimo_by_id(db, emprestimo_id)
    db_emprestimo.status = emprestimo.status
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo

def check_usuario(db: Session, usuario: schemas.UsuarioLoginSchema):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_usuario is None:
        return False
    return bcrypt.checkpw(usuario.senha.encode('utf8'), db_usuario.senha.encode('utf8'))

