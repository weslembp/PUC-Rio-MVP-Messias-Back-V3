from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base

class Chassi(Base):
    __tablename__ = 'chassi'

    numero_ordem = Column(Integer, primary_key=True, autoincrement=False)
    ordem_id = Column(Integer, ForeignKey("ordem_producao.id"), nullable=False)
    codigo_chassi = Column(String(100), nullable=False)

    ordem_rel = relationship("OrdemDeProducao", back_populates="chassi_rel")

    def __init__(self, numero_ordem: int, ordem_id: int, codigo_chassi: str):
        self.numero_ordem = numero_ordem
        self.ordem_id = ordem_id
        self.codigo_chassi = codigo_chassi