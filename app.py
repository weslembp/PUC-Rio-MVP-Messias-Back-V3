from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from model import Session, Produto, OrdemDeProducao, Chassi
from logger import logger
from schemas import *
from flask_cors import CORS
import requests
import math


MOCKAROO_API_KEY      = '' #COLOCAR APIKEY
URL_LISTAR_MOCKAROO   = f'https://api.mockaroo.com/api/6ac3abc0?&key={MOCKAROO_API_KEY}'
URL_CRIAR_MOCKAROO    = f'https://api.mockaroo.com/api/datasets/CARROS?key={MOCKAROO_API_KEY}'
URL_DELETAR_MOCKAROO  = 'https://my.api.mockaroo.com/deletecar'
URL_CHASSIS_MOCKAROO  = 'https://my.api.mockaroo.com/GenerateChassis'


info = Info(title="Messias API", version="3.0.0")
app  = OpenAPI(__name__, info=info)
CORS(app)

home_tag          = Tag(name="Documentação",
                        description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

produto_tag       = Tag(name="Produto [local]",
                        description="Adição, visualização e remoção de Produtos no banco local")

ordem_producao_tag = Tag(name="OrdemDeProducao [local]",
                         description="Criação e listagem de Ordens de Produção no banco local")

chassi_tag        = Tag(name="Chassi [local]",
                        description="Consulta e persistência de chassis no banco local")

mockaroo_veiculo_tag = Tag(
    name="Veículo [Mockaroo]",
    description=(
        "Rota do FRONT"
    )
)

mockaroo_chassi_tag = Tag(
    name="Chassi [Mockaroo]",
    description=(
        "Rota do FRONT"
    )
)

@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Lista todos os produtos cadastrados no banco local.
    """
    logger.debug("Coletando produtos do banco local...")
    session = Session()
    produtos = session.query(Produto).all()
    session.close()
    if not produtos:
        return {"produtos": []}, 200
    return apresenta_produtos(produtos), 200


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(body: ProdutoSchema):
    """Registra um produto no banco local.
    """
    produto = Produto(
        pk_produto=body.id,
        veiculo=body.veiculo,
        facelift=body.facelift,
        modelo=body.modelo
    )
    try:
        session = Session()
        session.add(produto)
        session.commit()
        return apresenta_produto(produto), 200
    except IntegrityError as e:
        session.rollback()
        return {"mesage": "Produto já salvo na base :/"}, 409
    except Exception as e:
        session.rollback()
        return {"mesage": f"Não foi possível salvar novo item: {str(e)}"}, 400
    finally:
        session.close()


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Remove um produto do banco local pelo seu id.
    """
    produto_id = query.id
    session = Session()
    count = session.query(Produto).filter(Produto.pk_produto == produto_id).delete()
    session.commit()
    session.close()
    if count:
        return {"mesage": "Produto removido", "nome": str(produto_id)}
    error_msg = "Produto não encontrado na base :/"
    logger.warning(f" #{produto_id} deu ruim")
    return {"mesage": error_msg}, 404


@app.get('/ordens_producao', tags=[ordem_producao_tag],
         responses={"200": ListagemOrdensSchema, "404": ErrorSchema})
def get_ordens_producao():
    """Lista todas as Ordens de Produção registradas no banco local.
    """
    session = Session()
    ordens = session.query(OrdemDeProducao).all()
    if not ordens:
        return {"ordens": []}, 200
    logger.debug(f"{len(ordens)} ordens encontradas")
    return apresenta_ordens_producao(ordens), 200


@app.post('/ordem_producao', tags=[ordem_producao_tag],
          responses={"200": OrdemDeProducaoViewSchema, "400": ErrorSchema})
def add_ordem_producao(body: OrdemDeProducaoSchema):
    """Cria uma nova Ordem de Produção no banco local.
    """
    session = Session()
    try:
        produto = session.query(Produto).filter(Produto.pk_produto == body.produto_id).first()
        if not produto:
            logger.debug(f"Produto #{body.produto_id} não encontrado. Criando automaticamente...")
            produto = Produto(
                pk_produto=body.produto_id,
                veiculo=body.veiculo,
                modelo=body.modelo,
                facelift=body.facelift
            )
            session.add(produto)
            session.flush()
        nova_op = OrdemDeProducao(
            produto_id=body.produto_id,
            quantidade_prevista=body.quantidade_prevista
        )
        session.add(nova_op)
        session.commit()
        return apresenta_ordem_producao(nova_op), 200
    except Exception as e:
        session.rollback()
        return {"mesage": f"Não foi possível salvar nova OP: {str(e)}"}, 400
    finally:
        session.close()


@app.get('/chassis', tags=[chassi_tag],
         responses={"200": ListagemChassisSchema, "404": ErrorSchema})
def get_chassis():
    """Lista todos os chassis persistidos no banco local.

    Os chassis são gerados externamente via PUT /mockaroo/chassis
    e armazenados aqui
    """
    session = Session()
    lista = session.query(Chassi).all()
    session.close()
    return apresenta_chassis(lista), 200


@app.put('/chassi', tags=[chassi_tag],
         responses={"200": ChassiViewSchema, "400": ErrorSchema})
def upsert_chassi(body: ChassiSchema):
    """Cria ou atualiza um chassi no banco local.

    Chamado internamente pela rota PUT /mockaroo/chassis após receber
    os dados gerados pelo Mockaroo.
    """
    session = Session()
    try:
        chassi = session.query(Chassi).filter(
            Chassi.numero_ordem == body.numero_ordem
        ).first()
        if chassi:
            chassi.codigo_chassi = body.codigo_chassi
            chassi.ordem_id = body.ordem_id
        else:
            chassi = Chassi(
                numero_ordem=body.numero_ordem,
                ordem_id=body.ordem_id,
                codigo_chassi=body.codigo_chassi
            )
            session.add(chassi)
        session.commit()
        return apresenta_chassi(chassi), 200
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao salvar chassi: {e}")
        return {"mesage": f"Erro ao salvar chassi: {str(e)}"}, 400
    finally:
        session.close()




@app.get('/mockaroo/veiculos', tags=[mockaroo_veiculo_tag],
         responses={"200": ListagemVeiculosMockarooSchema, "502": ErrorSchema})
def mockaroo_listar_veiculos():
    """[Mockaroo] Lista todos os veículos do dataset CARROS.
    """
    try:
        resp = requests.get(URL_LISTAR_MOCKAROO, timeout=10)
        resp.raise_for_status()
        return resp.json(), 200
    except Exception as e:
        logger.error(f"Erro ao consultar Mockaroo (listar veículos): {e}")
        return {"mesage": f"Falha ao consultar Mockaroo: {str(e)}"}, 502


@app.post('/mockaroo/veiculo', tags=[mockaroo_veiculo_tag],
          responses={"200": ProdutoViewSchema, "502": ErrorSchema, "400": ErrorSchema})
def mockaroo_criar_veiculo(body: VeiculoMockarooSchema):
    """[Mockaroo + banco local] Cria um veículo no Mockaroo e sincroniza o banco local.
    """
    facelift = f"FL{body.id}"
    csv_body  = f"id,Montadora,Modelo,Ano_Fabricacao\n{body.id},{body.montadora},{body.modelo},{body.ano_fabricacao}"
    dados_local = {
        "id":       body.id,
        "veiculo":  body.montadora,
        "modelo":   body.modelo,
        "facelift": facelift
    }

    try:
        resp_mock = requests.post(
            URL_CRIAR_MOCKAROO,
            headers={"Content-Type": "text/plain"},
            data=csv_body,
            timeout=10
        )
        resp_local = requests.post(
            "http://localhost:5000/produto",
            json=dados_local,
            timeout=10
        )

        if resp_mock.ok and resp_local.ok:
            return resp_local.json(), 200

        logger.error(f"Mockaroo: {resp_mock.status_code} | Local: {resp_local.status_code}")
        return {"mesage": "Erro ao sincronizar veículo entre Mockaroo e banco local."}, 502

    except Exception as e:
        logger.error(f"Erro ao criar veículo via proxy: {e}")
        return {"mesage": f"Falha no proxy: {str(e)}"}, 400


@app.delete('/mockaroo/veiculo', tags=[mockaroo_veiculo_tag],
            responses={"200": VeiculoDeleteResponseSchema, "502": ErrorSchema, "404": ErrorSchema})
def mockaroo_deletar_veiculo(query: VeiculoDeleteQuerySchema):
    """[Mockaroo + banco local] Remove um veículo do Mockaroo e do banco local.
    """
    produto_id = query.id
    try:
        resp_delete = requests.delete(
            URL_DELETAR_MOCKAROO,
            headers={"X-API-Key": MOCKAROO_API_KEY},
            timeout=10
        )
        resp_limpa = requests.post(
            URL_CRIAR_MOCKAROO,
            headers={"content-type": "text/plain"},
            data="id,Montadora,Modelo,Ano_Fabricacao",
            timeout=10
        )
        resp_local = requests.delete(
            f"http://localhost:5000/produto?id={produto_id}",
            timeout=10
        )

        if resp_delete.ok and resp_limpa.ok and resp_local.ok:
            return {"mesage": "Veículo removido do Mockaroo e do banco local.", "id": produto_id}, 200

        logger.error(
            f"deletecar: {resp_delete.status_code} | "
            f"limpar: {resp_limpa.status_code} | "
            f"local: {resp_local.status_code}"
        )
        return {"mesage": "Erro em uma ou mais etapas da deleção. Verifique os logs."}, 502

    except Exception as e:
        logger.error(f"Erro ao deletar veículo via proxy: {e}")
        return {"mesage": f"Falha no proxy: {str(e)}"}, 502


@app.put('/mockaroo/chassis', tags=[mockaroo_chassi_tag],
         responses={"200": ListagemChassisGeradosSchema, "502": ErrorSchema})
def mockaroo_gerar_chassis():
    """[Mockaroo + banco local] Gera chassis para todas as OPs e persiste no banco.

    O campo `numero_ordem` é um contador global sequencial entre todas as OPs.

    **Mockaroo endpoint:** `PUT https://my.api.mockaroo.com/GenerateChassis`
    """
    try:
        resp_ordens = requests.get("http://localhost:5000/ordens_producao", timeout=10)
        ordens = resp_ordens.json().get("ordens", [])
    except Exception as e:
        return {"mesage": f"Falha ao buscar OPs: {str(e)}"}, 502

    chassis_gerados = []
    numero_ordem_global = 1

    for ordem in ordens:
        try:
            resp_mock = requests.put(
                URL_CHASSIS_MOCKAROO,
                headers={
                    "X-API-Key":    MOCKAROO_API_KEY,
                    "Content-Type": "application/json"
                },
                json={"orderQuantity": str(ordem["quantidade_prevista"])},
                timeout=15
            )
            csv_text = resp_mock.text
            linhas   = csv_text.strip().split('\n')[1:]  # pula cabeçalho

            for linha in linhas:
                codigo_chassi = linha.split(',')[0]

                requests.put(
                    "http://localhost:5000/chassi",
                    json={
                        "numero_ordem":  numero_ordem_global,
                        "ordem_id":      ordem["id"],
                        "codigo_chassi": codigo_chassi
                    },
                    timeout=10
                )

                chassis_gerados.append({
                    "numero_ordem":  numero_ordem_global,
                    "ordem_id":      ordem["id"],
                    "codigo_chassi": codigo_chassi
                })
                numero_ordem_global += 1

        except Exception as e:
            logger.error(f"Erro ao processar OP {ordem['id']}: {e}")

    return {"chassis": chassis_gerados}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)