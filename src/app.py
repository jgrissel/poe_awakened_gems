from flask import Flask, render_template, jsonify
from calculator import calculate_profitability
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Simple in-memory cache
cache = {
    "data": [],
    "last_updated": None
}

from flask import Flask, render_template, jsonify, request
from calculator import calculate_profitability
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Simple in-memory cache
cache = {
    "data": [],
    "last_updated": None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    league = request.args.get('league', 'Keepers')
    data = calculate_profitability(league)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
