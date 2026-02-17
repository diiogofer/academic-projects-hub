# Imports
import os
from flask import Flask, jsonify, request
from psycopg_pool import ConnectionPool
import psycopg
from psycopg import errors
import re # para verificar input
from logging.config import dictConfig
import random

# Configurações do Flask e do psycopg
app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://postgres:postgres@postgres/Aviacao")
pool = ConnectionPool(
    conninfo = DATABASE_URL,
    kwargs = {
        "autocommit": True, # If True don’t start transactions automatically.
    },
    min_size = 4, max_size = 10, timeout = 5,
    open = True,
    name = "postgres_pool",
)
log = app.logger

# Estrutura do JSON
def create_response(message, status, dados):
    '''Cria uma resposta com um JSON com mensagem, status e os dados de resposta'''
    payload = {
        "message": message,
        "status": status,
        "dados": dados
    }
    return jsonify(payload)

# Middlewares
AEROPORTO_CODE_REGEX = re.compile(r'^[A-Z]{3}$')
def validate_aeroporto(code: str):
    """ Valida o código de um aeroporto baseado no seu REGEX """
    return bool(AEROPORTO_CODE_REGEX.fullmatch(code))
def validate_nif(nif: str):
    """ Valida o nif baseado na sua existência e no seu tamanho """
    return bool(nif) and len(nif) <= 9
def validate_voo(valor):
    """ Valida o voo id, confirmando que é um número inteiro """
    try:
        int(valor)
        return True
    except (ValueError, TypeError):
        return False

# Rotas
@app.route("/", methods=("GET",))
def list_airports():
    """
    GET /
    Lista todos os aeroportos (nome e cidade).
    
    Returns:
        Lista de dicionários com chaves:
            - nome: nome do aeroporto
            - cidade: cidade do aeroporto
        e com status code 200

    Raises:
        psycopg.OperationalError: "An error related to the database’s operation." (503)
        psycopg.DatabaseError: "Exception raised for errors that are related to the database." (503)
        Exception: qualquer outro erro. (500)
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                airports = cur.execute(
                    """
                    SELECT nome, cidade 
                    FROM aeroporto;
                    """
                ).fetchall()
        if not airports:
            return create_response("Não há aeroportos.", "OK", {}), 200
        dados = {"Aeroportos": [{"nome": name, "cidade": city} for name, city in airports]}
        return create_response("", "OK", dados), 200
    except (psycopg.OperationalError, psycopg.DatabaseError) as e:
        log.error("Database error in list_airports", exc_info = e) # Log inclui traceback
        return create_response("Error related with the Database", "error", {}), 503
    except Exception as e:
        log.error("Unexpected error in list_airports", exc_info = e)
        return create_response("Internal server error", "error", {}), 500

@app.route("/voos/<partida>", methods=("GET",))
def list_flights(partida):
    ''' 
        GET /voos/<partida>
        Lista todos os voos (número de série do avião, hora de partida e aeroporto de chegada) 
        que partem do aeroporto de <partida> até 12h após o momento da consulta.

        Args:
            partida: codigo de um aeroporto de partida
        Returns:
            JSON com lista de dicionários com chaves:
                - chegada: código do aeroporto de chegada
                - hora_partida: hora de partida
                - no_serie: número de série do avião
            com status code 200,
            ou 400, caso a validação de <partida> falhe.
        Raises:
            psycopg.OperationalError: "An error related to the database’s operation." (503)
            psycopg.DatabaseError: "Exception raised for errors that are related to the database." (503)
            Exception: qualquer outro erro. (500)
    '''
    # Validação do parametro <partida> recebido
    if not validate_aeroporto(partida):
        return create_response(f"Código de aeroporto inválido ({partida}): Deve ser 3 letras maiúsculas.", "error", {}), 400
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur: 
                # Sem Transação
                aeroporto = cur.execute(
                    """
                    SELECT 1 
                    FROM aeroporto 
                    WHERE codigo = %s;
                    """, 
                    (partida,),
                    ).fetchone()    
                if not aeroporto:
                    return create_response(f"Aeroporto {partida} não existe.", "error", {}), 404     
                flights = cur.execute(
                    """
                    SELECT  no_serie, hora_partida, chegada 
                    FROM voo 
                    WHERE partida = (%s) 
                        AND hora_partida > CURRENT_TIMESTAMP 
                        AND hora_partida <= CURRENT_TIMESTAMP + INTERVAL '12 hours'
                    ORDER BY hora_partida;
                    """, 
                    (partida,),
                ).fetchall()
        if not flights:
            return create_response(f"Não há voos disponíveis nas próximas 12h com partida em {partida}", "OK", {"voos": []}), 200
        dados = {"voos": [{"no_serie": no_serie, "hora_partida": hora_partida, "chegada": chegada} for no_serie, hora_partida, chegada in flights]}
        return create_response("", "OK",dados), 200
    except (psycopg.OperationalError, psycopg.DatabaseError) as e:
        log.error("Database error in list_flights", exc_info = e)
        return create_response("Erro relacionado à base de dados", "error", {}), 503
    except Exception as e:
        log.error("Unexpected error in list_flights", exc_info = e)
        return create_response("Erro inesperado no servidor", "error", {}), 500

@app.route("/voos/<partida>/<chegada>/", methods=("GET",))
def list_3_flights_with_remaining_tickets(partida, chegada):
    '''
        GET /voos/<partida>/<chegada>
        Lista os próximos três voos (número de série do avião e hora de partida) 
        entre o aeroporto de <partida> e o aeroporto de <chegada> para os quais 
        ainda há bilhetes disponíveis. 

        Args:
            partida: código de um aeroporto de partida
            chegada: código de um aeroporto de chegada
        Returns:
            lista de dicionários com chaves:
                - hora_partida: hora de partida
                - no_serie: número de série do avião
            ou 400, caso a validação de <partida> ou <chegada> falhe.
        Raises:
            psycopg.OperationalError: "An error related to the database’s operation." (503)
            psycopg.DatabaseError: "Exception raised for errors that are related to the database." (503)
            Exception: qualquer outro erro. (500)
    '''
     # Validação dos parâmetros recebidos
    if not validate_aeroporto(partida):
        return create_response(f"Código de aeroporto inválido ({partida}): Deve ser 3 letras maiúsculas.", "error", {}), 400
    if not validate_aeroporto(chegada):
        return create_response(f"Código de aeroporto inválido ({chegada}): Deve ter 3 letras maiúsculas.", "error", {}), 400
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                flights = cur.execute(
                    """
                    SELECT v.no_serie, v.hora_partida
                    FROM voo v
                    WHERE v.partida = (%s) AND v.chegada = (%s)
                        AND v.hora_partida > CURRENT_TIMESTAMP
                        AND (
                        (SELECT COUNT(*) FROM assento a WHERE v.no_serie = a.no_serie)
                        -
                        (SELECT COUNT(*) FROM bilhete b WHERE b.voo_id = v.id)
                        ) > 0
                    ORDER BY v.hora_partida
                    LIMIT 3;
                    """, 
                    (partida, chegada),
                ).fetchall() 
        if not flights:
            return create_response(f"Não existem voos com bilhetes disponíveis entre {partida} e {chegada}", "OK", {"voos": []}), 200
        dados = {"voos": [{"no_serie:": no_serie, "hora_partida": hora_partida} for no_serie, hora_partida in flights]}
        return create_response("", "OK", dados), 200
    except (psycopg.OperationalError, psycopg.DatabaseError) as e:
        log.error("Database error in list_3_flights_with_remaining_tickets", exc_info = e)
        return create_response("Erro ralacionado à base de dados","error", {}), 503
    except Exception as e:
        log.error("Unexpected error in list_3_flights_with_remaining_tickets", exc_info = e)
        return create_response("Erro inesperado no servidor", "error", {}), 500
    
@app.route("/compra/<voo>/", methods=("POST",))
def buy_one_or_more_tickets(voo):
    '''
    POST /compra/<voo>
    Faz uma compra de um ou mais bilhetes para o <voo>, populando as tabelas 
    <venda> e <bilhete>. Recebe como argumentos o nif do cliente, e uma lista 
    de pares (nome de passageiro, classe de bilhete) especificando os bilhetes a comprar.

    JSON body tem de seguir o formato:
    {
        "nif_cliente": ...,
        "bilhetes": [
            {"nome_passegeiro": ... , "prim_classe": ... },
            {"nome_passegeiro": ... , "prim_classe": ... },
            ...
        ]
    }

    Args:
        voo: id do voo

    Returns:
        201 Created ou 400 caso o post request esteja mal formatado
        e um JSON com uma mensagem informativa e um 
    Raises:
        errors.RaiseException: Provavelmente devido a um trigger (410)
        errors.ForeignKeyViolation: Violação de uma chave estrangeira (409)
        errors.UniqueViolation: Violação de uma unique constraint (409)
        psycopg.OperationalError: "An error related to the database’s operation." (503)
        psycopg.DatabaseError: "Exception raised for errors that are related to the database." (503)
        Exception: qualquer outro erro. (500)
    '''
    # Check body
    if not validate_voo(voo):
        return create_response(f"'{voo}' deve ser um identificador de um voo", "error", {}), 400
    pedido = request.get_json(silent=True) # silent = True -> Caso falhe nao lança erro, 
    if pedido is None:
        return create_response("JSON do request inválido: deve seguir o formato especificado na documentação", "error", {}), 400
    nif_cliente = pedido.get("nif_cliente", {})
    bilhetes = pedido.get("bilhetes", {}) 
    error = None 
    if not validate_nif(nif_cliente):
        error = "'nif_cliente' é inválido. Tem de ter 9 ou menos caracteres."
    if not bilhetes:
        error = "'bilhetes' tem de fazer parte do pedido."
    if error is not None:
        return create_response(error, "error", {}), 400
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Database Transction
                with conn.transaction():         
                    # Inserir a Venda
                    cur.execute(
                        """
                        INSERT INTO venda (nif_cliente, balcao, hora)
                        VALUES ((%s), NULL, CURRENT_TIMESTAMP)
                        RETURNING codigo_reserva;
                        """, (nif_cliente,),
                    )           
                    venda_id = cur.fetchone()[0]

                    for b in bilhetes:
                        # Cálculo de preço do bilhete
                        if b["prim_classe"]:
                            price = random.randint(150, 300)
                        else:
                            price = random.randint(50, 100)
                        
                        # Inserir o bilhete
                        cur.execute(
                            """
                            INSERT INTO bilhete (voo_id, codigo_reserva, nome_passegeiro, preco, prim_classe)
                            VALUES ((%s), (%s), (%s), (%s), (%s)); 
                            """, 
                            (voo, venda_id, b["nome_passegeiro"], price, b["prim_classe"]),
                        )
        return create_response("Successful purchase", "OK", {}), 201
    except errors.RaiseException as e:
        log.error("A trigger may have been activated in buy_one_or_more_tickets", exc_info = e)
        return create_response(e.diag.message_primary or "Confirme a consistência dos dados inseridos", "error", {}), 410 # "Condição tende a ser permanente"
    except errors.ForeignKeyViolation as e:
        log.error("Foreign key violation in buy_one_or_more_tickets", exc_info = e)
        return create_response("Confirme a consistência dos dados inseridos", "error", {}), 409
    except errors.UniqueViolation as e:
        log.error("Unique violation in buy_one_or_more_tickets", exc_info = e)
        return create_response("O nome de passageiro tem de ser único para a mesma venda para o mesmo voo.", "error", {}), 409
    except (psycopg.OperationalError, psycopg.DatabaseError) as e:
        log.error("Database error in buy_one_or_more_tickets", exc_info = e)
        return create_response("Erro ralacionado à base de dados", "error", {}), 503
    except Exception as e:
        log.error("Unexpected error in buy_one_or_more_tickets", exc_info = e)
        return create_response("Erro inesperado no servidor", "error", {}), 500

@app.route('/checkin/<bilhete>/', methods=("PATCH",))
def check_in(bilhete):
    """
    PATCH /checkin/<bilhete>/
    Faz o check-in de um bilhete, atribuindo-lhe automaticamente um assento da classe correspondente.

    Args:
        bilhete: id do bilhete a ser check-in
    Returns:
        JSON com mensagem informativa e status code 200 em caso de sucesso 
        ou 404 caso o recurso não seja encontrado
        ou 422 caso o bilhete já esteja check-in
    Raises:
        errors.RaiseException: Provavelmente devido a um trigger (400)
        psycopg.IntegrityError: Para violações de restrições de integridade (409)
        psycopg.OperationalError: "An error related to the database’s operation." (503)
        psycopg.DatabaseError: "Exception raised for errors that are related to the database." (503)
        Exception: qualquer outro erro. (500)
    """
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                with conn.transaction():
                    # Pega no bilhete
                    cur.execute(
                        """
                        SELECT b.voo_id, b.prim_classe, b.lugar, b.no_serie
                        FROM bilhete b 
                        WHERE b.id = (%s)
                        FOR UPDATE;
                        """, (bilhete,),
                    )       
                    # Retira o voo_id, classe, lugar e no_serie 
                    bilhete_check = cur.fetchone()
                    if bilhete_check is None:
                        return create_response("Bilhete não encontrado", "error", {}), 404
                    voo_id, classe, lugar_check, no_serie_check = bilhete_check
                    if voo_id is None or classe is None:
                        return create_response("Bilhete não encontrado", "error", {}), 404
                    if lugar_check or no_serie_check:
                        return create_response("O bilhete já foi checked-in.", "error", {}), 422
                    # Sabendo o voo id sabemos o avião (no_serie)
                    cur.execute(
                        """
                        SELECT v.no_serie FROM voo v 
                        WHERE v.id = (%s)
                        FOR UPDATE;
                        """, (voo_id,),
                    )
                    no_serie = cur.fetchone()[0]
                    if not no_serie:
                        return create_response("'voo' não foi encontrado.", "error", {}), 404
                    # Sebendo o avião, sabemos os lugares
                    # Nota sobre o lock: O lock é obtido depois do LIMIT 1.
                    cur.execute(
                        """
                        SELECT a.lugar 
                        FROM assento a 
                        WHERE a.no_serie = (%s) AND a.prim_classe = (%s)
                        AND NOT EXISTS (
                            SELECT 1 FROM bilhete b
                            WHERE b.voo_id = (%s) AND b.lugar = a.lugar
                        )
                        FOR UPDATE SKIP LOCKED
                        LIMIT 1;
                        """, (no_serie, classe, voo_id,),
                    ) 
                    lugar = cur.fetchone()[0]
                    if not lugar:
                        return create_response("'lugar' não foi encontrado", "error", {}), 404
                    # Faz update
                    cur.execute(
                        """
                        UPDATE bilhete 
                        SET lugar = (%s), no_serie = (%s)
                        WHERE id = (%s)
                        """, (lugar,no_serie,bilhete,),
                    )
        return create_response("Check-in completed successfully.","OK", {}), 200
    except errors.RaiseException as e:
        log.error("A trigger may have been activated in check_in", exc_info = e)
        return create_response(e.diag.message_primary or "Confirme a consistência dos dados inseridos", "error", {}), 400
    except psycopg.IntegrityError as e:
        log.error("Data may be inconsistent in check_in", exc_info = e)
        return create_response("Confirme a consistência dos dados inseridos", "error", {}), 409
    except (psycopg.OperationalError, psycopg.DatabaseError) as e:
        log.error("Database error in buy_one_or_more_tickets", exc_info = e)
        return create_response("Erro ralacionado à base de dados", "error", {}), 503
    except Exception as e:
        log.error("Unexpected error in buy_one_or_more_tickets", exc_info = e)
        return create_response("Erro inesperado no servidor", "error", {}), 500

# Main
if __name__ == "__main__":
    app.run()