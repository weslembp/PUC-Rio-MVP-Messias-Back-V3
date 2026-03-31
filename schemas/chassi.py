from pydantic import BaseModel
from typing import List
from model.chassi import Chassi

class ChassiSchema(BaseModel):
    """Define como um Chassi deve ser enviado (PUT)"""
    numero_ordem: int
    ordem_id: int
    codigo_chassi: str

class ChassiViewSchema(BaseModel):
    """Define como um Chassi será retornado"""
    numero_ordem: int
    ordem_id: int
    codigo_chassi: str

class ListagemChassisSchema(BaseModel):
    """Define como uma lista de chassis será retornada"""
    chassis: List[ChassiViewSchema]

def apresenta_chassi(c: Chassi):
    return {
        "numero_ordem": c.numero_ordem,
        "ordem_id": c.ordem_id,
        "codigo_chassi": c.codigo_chassi,
    }

def apresenta_chassis(lista: List[Chassi]):
    return {"chassis": [apresenta_chassi(c) for c in lista]}