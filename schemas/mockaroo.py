from pydantic import BaseModel
from typing import List, Optional


# ──────────────────────────────────────────────
#  Veículos (dataset CARROS no Mockaroo)
# ──────────────────────────────────────────────

class VeiculoMockarooSchema(BaseModel):
    """Payload enviado ao Mockaroo para criar um veículo no dataset CARROS.
    O frontend gera um id aleatório e monta o CSV internamente antes de enviar."""
    id: int
    montadora: str
    modelo: str
    ano_fabricacao: int


class VeiculoMockarooViewSchema(BaseModel):
    """Representação de um veículo retornado pelo Mockaroo (dataset CARROS)."""
    id: int
    Montadora: str
    Modelo: str
    Ano_Fabricacao: int
    FaceliftID: str


class ListagemVeiculosMockarooSchema(BaseModel):
    """Lista de veículos retornada pelo Mockaroo."""
    veiculos: List[VeiculoMockarooViewSchema]


class VeiculoDeleteQuerySchema(BaseModel):
    """Parâmetro de query para deleção de veículo (id do Mockaroo)."""
    id: int


class VeiculoDeleteResponseSchema(BaseModel):
    """Resposta após deleção de veículo no Mockaroo e no banco local."""
    mesage: str
    id: int


# ──────────────────────────────────────────────
#  Chassis (endpoint GenerateChassis no Mockaroo)
# ──────────────────────────────────────────────

class GerarChassisBodySchema(BaseModel):
    """Payload enviado ao Mockaroo para gerar chassis de uma OP.
    O campo orderQuantity controla quantos chassis são gerados."""
    ordem_id: int
    quantidade: float = 10.0


class ChassiGeradoSchema(BaseModel):
    """Representa um chassi gerado pelo Mockaroo e salvo no banco local."""
    numero_ordem: int
    ordem_id: int
    codigo_chassi: str


class ListagemChassisGeradosSchema(BaseModel):
    """Lista de chassis gerados e persistidos para todas as OPs."""
    chassis: List[ChassiGeradoSchema]