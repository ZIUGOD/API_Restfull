from flask import Flask, jsonify, request, make_response, abort
from database import database
from models.users import *
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config["DEBUG"] = True
app.json_encoder = UsersEncoder

auth = HTTPBasicAuth()  # inicializa o objeto de autenticação

# lista de usuários e senhas (para demonstração)
users = {
    "user1": "password1",
    "user2": "password2",
}


# função de autenticação
@auth.verify_password
def verify_password(username, password):
    if username in users and password == users[username]:
        return username


@app.route("/", methods=["GET"])
def home():
    return jsonify({"Pagina": "inicial"})


# mensagem de erro
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"Status": 404, "Error": "Resource not found."}), 404)
    # return render_template("error_page.html")


# cadastrar (Create)
@app.route("/local", methods=["POST"])
@auth.login_required  # protege a rota com autenticação
def create():
    if not request.json or not "nome" in request.json:
        abort(404)
    new_user = Local(
        request.json["nome"],
        request.json["endereco"],
        request.json["capacidade_maxima"],
    )
    database.append(new_user)
    return jsonify(new_user), 201  # status 201 == created


# selecionar todos (Read)
@app.route("/local", methods=["GET"])
def lists():
    return jsonify({"User": database, "Database": Local.__name__})


# selecionar apenas um (Read)
@app.route("/local/<int:id>", methods=["GET"])
def list(id):
    for local in database:
        if id == local.id:
            return jsonify(local)

    abort(404)


# atualizar (Update)
@app.route("/local/<int:id>", methods=["PUT"])
@auth.login_required  # protege a rota com autenticação
def update(id):
    if not request.json:
        abort(404)

    for local in database:
        if local.id == id:
            local.name = request.json["nome"]
            local.endereco = request.json["endereco"]
            local.capacidade_maxima = request.json["capacidade_maxima"]

            return jsonify({"Atualizado com sucesso!": True})

    abort(404)


# deletar (Delete)
@app.route("/local/<int:id>", methods=["DELETE"])
@auth.login_required  # protege a rota com autenticação
def delete(id):
    for local in database:
        if local.id == id:
            # delete
            database.remove(local)
            return jsonify({f"Local '{id}' excluído": True})

    abort(404)


if __name__ == "__main__":
    app.run()
