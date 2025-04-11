from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Colaborador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    unidade = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    colaborador = db.relationship('Colaborador', backref=db.backref('pedidos', lazy=True))

class PedidoProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    pedido = db.relationship('Pedido', backref=db.backref('itens', lazy=True))
    produto = db.relationship('Produto')

@app.route('/')
def index():
    pedidos = Pedido.query.order_by(Pedido.data.desc()).all()
    return render_template('index.html', pedidos=pedidos)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if request.method == 'POST':
        nome = request.form['nome']
        unidade = request.form['unidade']
        valor = float(request.form['valor'])

        novo_produto = Produto(nome=nome, unidade=unidade, valor=valor)
        db.session.add(novo_produto)
        db.session.commit()
        return redirect('/produtos')

    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

with app.app_context():
    db.create_all_
