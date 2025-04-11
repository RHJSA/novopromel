
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELOS
class Colaborador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    quantidade = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    pedidos = Pedido.query.order_by(Pedido.data.desc()).all()
    return render_template('index.html', pedidos=pedidos, Produto=Produto, Colaborador=Colaborador)

@app.route('/novo-pedido', methods=['GET', 'POST'])
def novo_pedido():
    if request.method == 'POST':
        colaborador_id = request.form['colaborador']
        produtos = request.form.getlist('produto')
        quantidades = request.form.getlist('quantidade')

        pedido = Pedido(colaborador_id=colaborador_id)
        db.session.add(pedido)
        db.session.commit()

        for prod_id, qtd in zip(produtos, quantidades):
            if int(qtd) > 0:
                item = ItemPedido(pedido_id=pedido.id, produto_id=prod_id, quantidade=int(qtd))
                db.session.add(item)

        db.session.commit()
        return redirect(url_for('index'))

    colaboradores = Colaborador.query.all()
    produtos = Produto.query.all()
    return render_template('novo_pedido.html', colaboradores=colaboradores, produtos=produtos)

@app.route('/cadastro-produto', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        db.session.add(Produto(nome=nome, preco=preco))
        db.session.commit()
        return redirect(url_for('cadastro_produto'))
    produtos = Produto.query.all()
    return render_template('cadastro_produto.html', produtos=produtos)

@app.route('/cadastro-colaborador', methods=['GET', 'POST'])
def cadastro_colaborador():
    if request.method == 'POST':
        nome = request.form['nome']
        db.session.add(Colaborador(nome=nome))
        db.session.commit()
        return redirect(url_for('cadastro_colaborador'))
    colaboradores = Colaborador.query.all()
    return render_template('cadastro_colaborador.html', colaboradores=colaboradores)

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        with app.app_context():
            db.create_all()
    app.run(host='0.0.0.0', port=10000)
