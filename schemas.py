from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class BairroBase(BaseModel):
    nome: str


class BairroCreate(BairroBase):
    pass


class Bairro(BairroBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CandidatoCreate(BaseModel):
    nome: str
    partido: str
    numero: int
    cargo: str


class Candidato(CandidatoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EntrevistaCreate(BaseModel):
    nome_votante: str
    pesquisador_nome: str
    bairro_id: int
    casa: str
    candidato_voto_id: int
    texto_anotacao: Optional[str] = None


class Entrevista(BaseModel):
    id: int
    nome_votante: str
    pesquisador_nome: str
    data_hora: datetime
    model_config = ConfigDict(from_attributes=True)
