from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes_storage = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes/', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        text = request.form.get('text', '').strip()
        if title and text:
            notes_storage[title] = text
        return redirect(url_for('notes'))
    return render_template('notes.html', notes=notes_storage)

if __name__ == '__main__':
    app.run(debug=True)
