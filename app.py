from flask import Flask, request, render_template
from rag_model import search
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_route():
    query = request.form['query']
    results = search(query)
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
