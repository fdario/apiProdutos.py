from flask import Flask, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import json
 
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/apiprodutos"

db = SQLAlchemy(app)

class Produtos2(db.Model):
 
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    preco_custo = db.Column(db.Float)
    preco_venda = db.Column(db.Float)
    unidade_embalagem = db.Column(db.String(2))
    qtd_embalagem = db.Column(db.Integer)
    cod_barra_embalagem = db.Column(db.Integer)

    # Ao iniciar, no prompt, criar a tabela com os comandos:
    # python
    # from app import db
    # db.create_all() 


    def to_json(self):
         return {
            "id": self.id,
            "descricao": self.descricao,
            "marca": self.marca,
            "preco de custo": self.preco_custo,
            "preco de venda": self.preco_venda,
            "unidade da embalagem": self.unidade_embalagem,
            "quantidade de embalagens": self.qtd_embalagem,
            "código de barras": self.cod_barra_embalagem
            }

#\/ inicio do frontend

# @app.route("/")
# def index():
#     return render_template('index.html')


#Listar todos
@app.route("/listaprodutos", methods=["GET"])
def lista_produtos():
    lista_produtos = Produtos2.query.all()
    produtos_json = [produto.to_json() for produto in lista_produtos]
    print(produtos_json)
    # mostrar = json.loads(json.dumps(produtos_json))
    # print(mostrar)

    return response (200, "produtos", produtos_json, "tudo certo")

#lista um produto, passando o id do produto na url
@app.route('/produto/<id>', methods=["GET"])
def seleciona_produto(id):
    produto = Produtos2.query.filter_by(id=id).first()
    produto_json = produto.to_json()
    return response (200, "produto", produto_json)

#adiciona o produto, passando o produto no corpo, com método POST
@app.route("/adicionarproduto", methods=["POST"])
def adiciona_produto():
    body = request.get_json()
    try:
        produto=Produtos2(
            id = body["id"],
            descricao = body["descricao"],
            marca = body["marca"],
            preco_custo = body["preco de custo"],
            preco_venda = body["preco de venda"],
            unidade_embalagem = body["unidade da embalagem"],
            qtd_embalagem = body["quantidade de embalagens"],
            cod_barra_embalagem = body["código de barras"],
        )
        db.session.add(produto)
        db.session.commit()
        return response (201, "produto", produto.to_json(), "produto adicionado")
    except Exception as e:
        print("erro ", e)
        return response (400, "produto", {}, "erro ao adicionar")
    
#atualiza o produto, passando o id do produto na url
@app.route("/produto/<id>", methods=["PUT"])
def atualizar_produto(id):
    produto = Produtos2.query.filter_by(id=id).first()
    body = request.get_json()
    try:
        if("descricao" in body):
            produto.descricao = body["descricao"]
        if("marca" in body):
            produto.marca = body["marca"]
        if("preco de custo" in body):
            produto.preco_custo = body["preco de custo"]
        if("preco de venda" in body):
            produto.preco_venda = body["preco de venda"]
        if("unidade da embalagem" in body):
            produto.unidade_embalagem = body["unidade da embalagem"]
        if("quantidade de embalagens" in body):
            produto.qtd_embalagem = body["quantidade de embalagem"]
        if("código de barras" in body):
            produto.cod_barra_embalagem = body["código de barras"]
        db.session.add(produto)
        db.session.commit()
        return response (201, "produto", produto.to_json(), "produto atualizado")
    except Exception as e:
        print("erro ", e)
        return response (400, "produto", {}, "erro ao atualizar")

#deleta o produto, passando o id do produto na url
@app.route("/produto/<id>", methods=["DELETE"])
def deleta_produto(id):
    produto = Produtos2.query.filter_by(id=id).first()
    try:
        db.session.delete(produto)
        db.session.commit()
        return response (200, "produto", produto.to_json(), "produto deletado")
    except Exception as e:
        print("Erro: ", e)
        return response (400, "produtos", {}, "erro ao deletar")

#método do response e código de status do json
def response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)