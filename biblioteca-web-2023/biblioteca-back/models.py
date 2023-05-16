from sqlalchemy import Column, Integer, String, SmallInteger, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    senha = Column(String(255))
    emprestimos = relationship("Emprestimo", back_populates="usuario")

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    
    id = Column(Integer, primary_key=True, index=True)
    data_retirada = Column(Date)
    status = Column(SmallInteger)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="emprestimos")
    livros = relationship("Livro", secondary="itens_emprestimo", back_populates='emprestimos')

class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150))
    resumo = Column(String(1000))
    emprestimos = relationship("Emprestimo", secondary="itens_emprestimo", back_populates='livros')

itens_emprestimo = Table('itens_emprestimo', Base.metadata,
    Column('id_livro', ForeignKey('livros.id'), primary_key=True),
    Column('id_emprestimo', ForeignKey('emprestimos.id'), primary_key=True)
)
