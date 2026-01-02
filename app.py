from flask import Flask, g 
from todos.database_persistence.py import DatabasePersistence

app = Flask(__name__)

@app.before_request
def load_storage():
    g.storage = DatabasePersistence()
    
@app.route("/")
def index():
    return "<h1>This is a todo starter!</h1>"

if __name__ == "__main__":
    app.run(debug=True, port=5003)