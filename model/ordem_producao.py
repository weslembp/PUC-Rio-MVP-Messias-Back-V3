from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from  model import Base 

class OrdemDeProducao(Base):
    __tablename__ = 'ordem_producao'

    id = Column(Integer, primary_key=True)
    # Este 'produto.pk_produto' deve bater com o nome da tabela e chave primária definida em produto.py
    produto_id = Column(Integer, ForeignKey("produto.pk_produto"), nullable=False)
    quantidade_prevista = Column(Float)
    status = Column(String(50), default='PENDENTE') 
    data_criacao = Column(DateTime, default=datetime.now())
    
    # O back_populates deve existir na classe Produto também
    produto_rel = relationship("Produto", back_populates="ordens_producao")
    chassi_rel = relationship("Chassi", back_populates="ordem_rel")
    def __init__(self, produto_id:int, quantidade_prevista:float, status:str='PENDENTE', data_criacao:Union[DateTime, None] = None):
        """
        Cria uma Ordem de Produção (OP)
        
        Arguments:
            produto_id: ID do produto a ser produzido (chave estrangeira).
            quantidade_prevista: Quantidade que deve ser produzida.
            status: Situação da OP (default: 'PENDENTE').
            data_criacao: Data de criação da OP.
        """
        self.produto_id = produto_id
        self.quantidade_prevista = quantidade_prevista
        self.status = status
        
        if data_criacao:
            self.data_criacao = data_criacao