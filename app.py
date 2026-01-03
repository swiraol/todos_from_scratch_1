from flask import Flask, g, redirect, render_template, url_for 
from todos.database_persistence import DatabasePersistence

app = Flask(__name__)

@app.before_request
def load_storage():
    g.storage = DatabasePersistence()

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists")
def get_lists():
    all_lists = g.storage.all_lists()
    return render_template('lists.html', lists=all_lists)

if __name__ == "__main__":
    app.run(debug=True, port=5003)