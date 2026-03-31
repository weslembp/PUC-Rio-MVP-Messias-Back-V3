# schemas/__init__.py
from schemas.produto import ProdutoSchema, ProdutoBuscaSchema, ProdutoViewSchema, \
                            ListagemProdutosSchema, ProdutoDelSchema, apresenta_produto, \
                            apresenta_produtos
from schemas.ordem_producao import OrdemDeProducaoSchema, OrdemDeProducaoViewSchema, \
                                   ListagemOrdensSchema, apresenta_ordens, \
                                   apresenta_ordem_producao, apresenta_ordens_producao  # <-- adicionado aqui
from schemas.error import ErrorSchema
from schemas.chassi import ChassiSchema, ChassiViewSchema, ListagemChassisSchema, \
                           apresenta_chassi, apresenta_chassis

from schemas.mockaroo import (
    VeiculoMockarooSchema, VeiculoMockarooViewSchema, ListagemVeiculosMockarooSchema,
    VeiculoDeleteQuerySchema, VeiculoDeleteResponseSchema,
    GerarChassisBodySchema, ListagemChassisGeradosSchema, ChassiGeradoSchema
)