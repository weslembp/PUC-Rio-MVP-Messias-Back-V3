from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base
import random

class Produto(Base):
    __tablename__ = 'produto'

    pk_produto = Column("pk_produto", Integer, primary_key=True, autoincrement=False)
    veiculo = Column(String(140))
    facelift = Column(String(140))
    modelo = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now)

    ordens_producao = relationship("OrdemDeProducao", back_populates="produto_rel")

    def __init__(self, pk_produto: int, veiculo: str, facelift: str, modelo: str, data_insercao: datetime = None):
        self.pk_produto = pk_produto # Recebe o ID que veio do parâmetro
        self.veiculo = veiculo
        self.facelift = facelift
        self.modelo = modelo
        if data_insercao:
            self.data_insercao = data_insercao