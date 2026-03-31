from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto

class ProdutoSchema(BaseModel):
    """ Define como um novo veículo deve ser representado """
    id: int 
    veiculo: str 
    facelift: Optional[str] = "N/A" 
    modelo: str

class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca (pelo modelo). """
    id: int

class ProdutoViewSchema(BaseModel):
    """ Define como o veículo será retornado """
    id: int = 1
    veiculo: str = "Honda Civic"
    facelift: str = "G10"
    modelo: str = "EXL 2.0"

class ProdutoDelSchema(BaseModel):
    """ Define a estrutura do dado retornado após a remoção """
    message: str
    veiculo: str

class ListagemProdutosSchema(BaseModel):
    """ Define a estrutura da lista de veículos """
    produtos: List[ProdutoViewSchema]

def apresenta_produtos(produtos: List[Produto]):
    result = []
    for p in produtos:
        result.append({
            "id": p.pk_produto, 
            "veiculo": p.veiculo,
            "facelift": p.facelift,
            "modelo": p.modelo,
        })
    return {"produtos": result}

def apresenta_produto(p: Produto):
    return {
        "id": p.pk_produto, 
        "veiculo": p.veiculo,
        "facelift": p.facelift,
        "modelo": p.modelo,
    }