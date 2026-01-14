from flask import Flask, g, redirect, render_template, request, url_for 
from todos.database_persistence import DatabasePersistence

app = Flask(__name__)

@app.before_request
def load_storage():
    g.storage = DatabasePersistence()

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists/")
def get_lists():
    all_lists = g.storage.all_lists()
    return render_template('lists.html', lists=all_lists)

@app.route("/lists/", methods=["POST"])
def create_list():
    title = request.form['list_title']
    g.storage.create_list(title)
    return redirect(url_for('get_lists'))

@app.route("/lists/new/")
def new_list():
    return render_template('new_list.html')

@app.route("/lists/<list_id>/")
def show_list(list_id):
    lst = g.storage.find_list(list_id)
    return render_template('list.html', lst=lst)

@app.route("/lists/<list_id>/edit/")
def edit_list(list_id):
    lst = g.storage.find_list(list_id)
    
    return render_template('edit_list.html', lst=lst)

@app.route("/lists/<list_id>/edit/", methods=["POST"])
def update_list(list_id):
    title = request.form['new_list_title']
    g.storage.edit_list(list_id, title)

    return redirect(url_for('show_list', list_id=list_id))
@app.route("/lists/<list_id>/delete/", methods=['POST'])
def delete_list(list_id):
    g.storage.delete_list(list_id)

    return redirect(url_for('get_lists'))

@app.route("/lists/<list_id>/todos/", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form['todo_title']
    g.storage.create_todo(list_id, todo_title)
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/todos/<todo_id>/delete/", methods=["POST"])
def delete_todo(list_id, todo_id):
    g.storage.delete_todo(list_id, todo_id)
    
    return redirect(url_for('show_list', list_id=list_id))

if __name__ == "__main__":
    app.run(debug=True, port=5003)