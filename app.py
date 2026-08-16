from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from flask_socketio import (
    SocketIO
)

from database import (
    conectar
)


app = Flask(__name__)

app.config[
    "SECRET_KEY"
] = "sistema-apresentacao"


socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)


# ==================================================
# PÁGINAS
# ==================================================

@app.route("/")
def controle():

    return render_template(
        "controle.html"
    )


@app.route("/projecao")
def projecao():

    return render_template(
        "projecao.html"
    )


# ==================================================
# APRESENTAÇÕES
# ==================================================

@app.route(
    "/api/apresentacoes",
    methods=["GET"]
)
def listar_apresentacoes():

    conexao = conectar()

    apresentacoes = conexao.execute(
        """
        SELECT *
        FROM apresentacoes
        ORDER BY id DESC
        """
    ).fetchall()

    conexao.close()


    return jsonify([
        dict(item)
        for item in apresentacoes
    ])


@app.route(
    "/api/apresentacoes",
    methods=["POST"]
)
def criar_apresentacao():

    dados = request.json

    nome = dados.get(
        "nome",
        "Nova apresentação"
    )

    descricao = dados.get(
        "descricao",
        ""
    )


    conexao = conectar()

    cursor = conexao.cursor()


    cursor.execute(
        """
        INSERT INTO apresentacoes
        (
            nome,
            descricao
        )
        VALUES (?, ?)
        """,
        (
            nome,
            descricao
        )
    )


    conexao.commit()

    id_apresentacao = cursor.lastrowid

    conexao.close()


    return jsonify({
        "sucesso": True,
        "id": id_apresentacao
    })


# ==================================================
# EXCLUIR APRESENTAÇÃO
# ==================================================

@app.route(
    "/api/apresentacoes/<int:id>",
    methods=["DELETE"]
)
def excluir_apresentacao(id):

    conexao = conectar()

    conexao.execute(
        """
        DELETE FROM slides
        WHERE apresentacao_id = ?
        """,
        (id,)
    )


    conexao.execute(
        """
        DELETE FROM apresentacoes
        WHERE id = ?
        """,
        (id,)
    )


    conexao.commit()

    conexao.close()


    return jsonify({
        "sucesso": True
    })


# ==================================================
# SLIDES
# ==================================================

@app.route(
    "/api/apresentacoes/<int:id>/slides",
    methods=["GET"]
)
def listar_slides(id):

    conexao = conectar()

    slides = conexao.execute(
        """
        SELECT *
        FROM slides
        WHERE apresentacao_id = ?

        ORDER BY ordem ASC
        """,
        (id,)
    ).fetchall()


    conexao.close()


    return jsonify([
        dict(slide)
        for slide in slides
    ])


# ==================================================
# CRIAR SLIDE
# ==================================================

@app.route(
    "/api/apresentacoes/<int:id>/slides",
    methods=["POST"]
)
def criar_slide(id):

    dados = request.json


    conexao = conectar()

    cursor = conexao.cursor()


    ordem = cursor.execute(
        """
        SELECT
            COALESCE(MAX(ordem), 0) + 1

        FROM slides

        WHERE apresentacao_id = ?
        """,
        (id,)
    ).fetchone()[0]


    cursor.execute(
        """
        INSERT INTO slides
        (
            apresentacao_id,
            titulo,
            texto,
            tamanho,
            cor_texto,
            cor_fundo,
            alinhamento,
            ordem
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            id,

            dados.get(
                "titulo",
                "Novo Slide"
            ),

            dados.get(
                "texto",
                ""
            ),

            dados.get(
                "tamanho",
                60
            ),

            dados.get(
                "cor_texto",
                "#ffffff"
            ),

            dados.get(
                "cor_fundo",
                "#000000"
            ),

            dados.get(
                "alinhamento",
                "center"
            ),

            ordem
        )
    )


    conexao.commit()

    slide_id = cursor.lastrowid

    conexao.close()


    return jsonify({
        "sucesso": True,
        "id": slide_id
    })


# ==================================================
# EDITAR SLIDE
# ==================================================

@app.route(
    "/api/slides/<int:id>",
    methods=["PUT"]
)
def editar_slide(id):

    dados = request.json


    conexao = conectar()


    conexao.execute(
        """
        UPDATE slides

        SET

            titulo = ?,

            texto = ?,

            tamanho = ?,

            cor_texto = ?,

            cor_fundo = ?,

            alinhamento = ?

        WHERE id = ?

        """,

        (

            dados.get(
                "titulo",
                ""
            ),

            dados.get(
                "texto",
                ""
            ),

            dados.get(
                "tamanho",
                60
            ),

            dados.get(
                "cor_texto",
                "#ffffff"
            ),

            dados.get(
                "cor_fundo",
                "#000000"
            ),

            dados.get(
                "alinhamento",
                "center"
            ),

            id

        )
    )


    conexao.commit()

    conexao.close()


    return jsonify({
        "sucesso": True
    })


# ==================================================
# EXCLUIR SLIDE
# ==================================================

@app.route(
    "/api/slides/<int:id>",
    methods=["DELETE"]
)
def excluir_slide(id):

    conexao = conectar()


    conexao.execute(
        """
        DELETE FROM slides
        WHERE id = ?
        """,
        (id,)
    )


    conexao.commit()

    conexao.close()


    return jsonify({
        "sucesso": True
    })


# ==================================================
# WEBSOCKET
# ==================================================

@socketio.on("exibir")
def exibir(dados):

    print(
        "Projetando:",
        dados
    )


    socketio.emit(
        "atualizar_projecao",
        dados
    )


@socketio.on("limpar")
def limpar():

    socketio.emit(
        "limpar_projecao"
    )


# ==================================================
# EXECUTAR
# ==================================================

if __name__ == "__main__":

    print("")
    print(
        "================================"
    )

    print(
        " SISTEMA DE APRESENTAÇÃO"
    )

    print(
        "================================"
    )

    print("")

    print(
        "Controle:"
    )

    print(
        "http://localhost:5000"
    )

    print("")

    print(
        "Projeção:"
    )

    print(
        "http://localhost:5000/projecao"
    )

    print("")


    socketio.run(

        app,

        host="0.0.0.0",

        port=5000,

        debug=True

    )