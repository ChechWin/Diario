from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

@app.route('/')
def index():
    cards = Card.query.order_by(Card.id).all()  # Obtener todas las tarjetas
    return render_template('index.html', cards=cards)

@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)  # Obtener la tarjeta por su ID
    return render_template('card.html', card=card)

@app.route('/create')
def create():
    return render_template('create_card.html')

@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        # Crear un objeto Card y agregarlo a la base de datos
        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()  # Guardar los cambios en la base de datos

        return redirect('/')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
