from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Bairro(Base):
    __tablename__ = "bairros"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    entrevistas = relationship(
        "Entrevista", back_populates="bairro_rel", cascade="all, delete-orphan"
    )


class Candidato(Base):
    __tablename__ = "candidatos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    partido = Column(String)
    numero = Column(Integer)
    cargo = Column(String)
    entrevistas = relationship("Entrevista", back_populates="candidato_rel")


class Entrevista(Base):
    __tablename__ = "entrevistas"
    id = Column(Integer, primary_key=True, index=True)
    nome_votante = Column(String)
    pesquisador_nome = Column(String)
    bairro_id = Column(Integer, ForeignKey("bairros.id"))
    casa = Column(String)
    candidato_voto_id = Column(Integer, ForeignKey("candidatos.id"))
    data_hora = Column(DateTime, default=datetime.utcnow)

    bairro_rel = relationship("Bairro", back_populates="entrevistas")
    candidato_rel = relationship("Candidato", back_populates="entrevistas")
    anotacao = relationship(
        "Anotacao",
        back_populates="entrevista",
        cascade="all, delete-orphan",
        uselist=False,
    )


class Anotacao(Base):
    __tablename__ = "anotacoes"
    id = Column(Integer, primary_key=True, index=True)
    entrevista_id = Column(Integer, ForeignKey("entrevistas.id"))
    texto_anotacao = Column(String)
    entrevista = relationship("Entrevista", back_populates="anotacao")
