from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Optional

import models, database
from schemas import (
    BairroCreate,
    Bairro,
    CandidatoCreate,
    Candidato,
    EntrevistaCreate,
    Entrevista,
)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Nice Research - API Profissional Completa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- BAIRROS ---
@app.post("/bairros/", response_model=Bairro, tags=["Bairros"])
def criar_bairro(bairro: BairroCreate, db: Session = Depends(database.get_db)):
    nome_limpo = bairro.nome.strip().upper()
    if db.query(models.Bairro).filter(models.Bairro.nome == nome_limpo).first():
        raise HTTPException(status_code=400, detail="Bairro já cadastrado.")
    novo = models.Bairro(nome=nome_limpo)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@app.get("/bairros/", response_model=List[Bairro], tags=["Bairros"])
def listar_bairros(db: Session = Depends(database.get_db)):
    return db.query(models.Bairro).all()


@app.delete("/bairros/{bairro_id}", tags=["Bairros"])
def remover_bairro(bairro_id: int, db: Session = Depends(database.get_db)):
    alvo = db.query(models.Bairro).get(bairro_id)
    if not alvo:
        raise HTTPException(status_code=404, detail="Bairro não encontrado.")
    db.delete(alvo)
    db.commit()
    return {"message": "Bairro removido"}


# --- CANDIDATOS ---
@app.post("/candidatos/", response_model=Candidato, tags=["Candidatos"])
def criar_candidato(candidato: CandidatoCreate, db: Session = Depends(database.get_db)):
    novo = models.Candidato(**candidato.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@app.get("/candidatos/", response_model=List[Candidato], tags=["Candidatos"])
def listar_candidatos(db: Session = Depends(database.get_db)):
    return db.query(models.Candidato).all()


@app.delete("/candidatos/{candidato_id}", tags=["Candidatos"])
def remover_candidato(candidato_id: int, db: Session = Depends(database.get_db)):
    alvo = db.query(models.Candidato).get(candidato_id)
    if not alvo:
        raise HTTPException(status_code=404, detail="Candidato não encontrado.")
    db.delete(alvo)
    db.commit()
    return {"message": "Candidato removido"}


# --- ENTREVISTAS (VOTOS) ---
@app.post("/entrevistas/", status_code=status.HTTP_201_CREATED, tags=["Votos"])
def registrar_voto(voto: EntrevistaCreate, db: Session = Depends(database.get_db)):
    if not db.query(models.Bairro).get(voto.bairro_id):
        raise HTTPException(status_code=400, detail="Bairro inválido.")
    if not db.query(models.Candidato).get(voto.candidato_voto_id):
        raise HTTPException(status_code=400, detail="Candidato inválido.")

    nova = models.Entrevista(
        nome_votante=voto.nome_votante,
        pesquisador_nome=voto.pesquisador_nome,
        bairro_id=voto.bairro_id,
        casa=voto.casa,
        candidato_voto_id=voto.candidato_voto_id,
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    if voto.texto_anotacao:
        anot = models.Anotacao(
            entrevista_id=nova.id, texto_anotacao=voto.texto_anotacao
        )
        db.add(anot)
        db.commit()
    return {"id": nova.id, "status": "sucesso"}


@app.get("/entrevistas/", response_model=List[Entrevista], tags=["Votos"])
def listar_votos(db: Session = Depends(database.get_db)):
    return db.query(models.Entrevista).all()


@app.delete("/entrevistas/{voto_id}", tags=["Votos"])
def remover_voto(voto_id: int, db: Session = Depends(database.get_db)):
    alvo = db.query(models.Entrevista).get(voto_id)
    if not alvo:
        raise HTTPException(status_code=404, detail="Voto não encontrado.")
    db.delete(alvo)
    db.commit()
    return {"message": "Voto removido"}


# --- INTELIGÊNCIA ---
@app.get("/ranking-geral/", tags=["Inteligência"])
def ranking(dias: Optional[int] = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Entrevista)
    if dias:
        query = query.filter(
            models.Entrevista.data_hora >= datetime.utcnow() - timedelta(days=dias)
        )
    total = query.count()
    candidatos = db.query(models.Candidato).all()
    res = []
    for c in candidatos:
        votos = query.filter(models.Entrevista.candidato_voto_id == c.id).count()
        res.append(
            {
                "nome": c.nome,
                "votos": votos,
                "porcentagem": f"{(votos/total*100) if total > 0 else 0:.2f}%",
            }
        )
    return {
        "total_votos": total,
        "ranking": sorted(res, key=lambda x: x["votos"], reverse=True),
    }


@app.get("/feed-qualitativo/", tags=["Inteligência"])
def feed(db: Session = Depends(database.get_db)):
    anotacoes = db.query(models.Anotacao).all()
    return [
        {"bairro": a.entrevista.bairro_rel.nome, "comentario": a.texto_anotacao}
        for a in anotacoes
    ]


@app.get("/cobertura-bairros/", tags=["Inteligência"])
def cobertura(db: Session = Depends(database.get_db)):
    bairros = db.query(models.Bairro).all()
    res = []
    for b in bairros:
        votos = (
            db.query(models.Entrevista)
            .filter(models.Entrevista.bairro_id == b.id)
            .count()
        )
        res.append({"bairro": b.nome, "entrevistas": votos})
    return sorted(res, key=lambda x: x["entrevistas"])
