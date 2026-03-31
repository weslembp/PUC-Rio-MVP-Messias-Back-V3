from pydantic import BaseModel
from typing import List
from model.ordem_producao import OrdemDeProducao

class OrdemDeProducaoSchema(BaseModel):
    produto_id: int = 1
    quantidade_prevista: float = 100.0
    veiculo: str = ""     
    modelo: str = ""     
    facelift: str = "N/A"

class OrdemDeProducaoViewSchema(BaseModel):
    """ Define como uma Ordem de Produção será retornada """
    id: int = 1
    produto_id: int = 1
    veiculo: str = "Honda Civic"
    modelo: str = "EXL 2.0"
    quantidade_prevista: float = 100.0
    status: str = 'PENDENTE'
    data_criacao: str = "20/11/2023 10:00:00"

class ListagemOrdensSchema(BaseModel):
    """ Define como uma listagem de Ordens de Produção será retornada. """
    ordens: List[OrdemDeProducaoViewSchema]

def apresenta_ordem_producao(ordem: OrdemDeProducao):
    """ Retorna a representação básica de uma Ordem de Produção. """
    return {
        "id": ordem.id,
        "produto_id": ordem.produto_id,
        "quantidade_prevista": ordem.quantidade_prevista,
        "status": ordem.status,
        "data_criacao": ordem.data_criacao.strftime('%d/%m/%Y %H:%M:%S')
    }

def apresenta_ordem_producao_com_detalhes(ordem_obj, veiculo: str, modelo: str):
    """ Retorna a representação de uma OP com detalhes do veículo vindo do Mockaroo/Local """
    return {
        "id": ordem_obj.id,
        "produto_id": ordem_obj.produto_id,
        "veiculo": veiculo, 
        "modelo": modelo,
        "quantidade_prevista": ordem_obj.quantidade_prevista,
        "status": ordem_obj.status,
        "data_criacao": ordem_obj.data_criacao.strftime('%d/%m/%Y %H:%M:%S')
    }

def apresenta_ordens(ordens: List[OrdemDeProducao]):
    """ Retorna uma listagem de ordens de produção. """
    result = []
    for ordem in ordens:
        result.append(apresenta_ordem_producao(ordem))
    return {"ordens": result}


def apresenta_ordens_producao(ordens: List[OrdemDeProducao]):
    """ Retorna uma representação de uma lista de Ordens de Produção. """
    result = []
    
    from model import Session, Produto
    session = Session()
    
    for ordem in ordens:

        produto = session.query(Produto).filter(Produto.pk_produto == ordem.produto_id).first()
        nome_veiculo = produto.veiculo if produto else "Veículo não encontrado"
        
        result.append({
            "id": ordem.id,
            "produto_id": ordem.produto_id,
            "veiculo": nome_veiculo, 
            "quantidade_prevista": ordem.quantidade_prevista,
            "status": ordem.status,
            "data_criacao": ordem.data_criacao.strftime('%d/%m/%Y %H:%M:%S')
        })
    
    session.close()
    return {"ordens": result}