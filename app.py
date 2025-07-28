from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # 6. Инициализация миграций

# 5. Изменение структуры БД с добавлением колонки subtitle
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes/', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subtitle = request.form.get('subtitle', '').strip()
        text = request.form.get('text', '').strip()
        if title and text:
            new_note = Notes(title=title, subtitle=subtitle if subtitle else None, text=text)
            db.session.add(new_note)
            db.session.commit()
        return redirect(url_for('notes'))
    all_notes = Notes.query.order_by(Notes.id.desc()).all()
    return render_template('notes.html', notes=all_notes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
