import secrets
from todos.utils import error_for_list_title
from flask import (
    flash, 
    Flask, 
    g, 
    redirect, 
    render_template, 
    request,  
    session, 
    url_for
)
from todos.database_persistence import DatabasePersistence

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

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
    all_lists = g.storage.all_lists()
    error = error_for_list_title(title, all_lists)
    if error:
        flash(error, 'error')
        return redirect(url_for('new_list'))
    g.storage.create_list(title)
    flash('You successfully created a new list', 'success')
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
    all_lists = g.storage.all_lists()
    error = error_for_list_title(title, all_lists)
    if error:
        flash(error, 'error')
        return redirect(url_for('edit_list', list_id=list_id))
    
    g.storage.edit_list(list_id, title)    
    flash('You successfully edited your list', 'success')
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/delete/", methods=['POST'])
def delete_list(list_id):
    g.storage.delete_list(list_id)
    flash('You successfully deleted the list', 'success')

    return redirect(url_for('get_lists'))

@app.route("/lists/<list_id>/todos/", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form['todo_title']
    g.storage.create_todo(list_id, todo_title)
    flash('You successfully created a todo item', 'success')
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/todos/<todo_id>/delete/", methods=["POST"])
def delete_todo(list_id, todo_id):
    g.storage.delete_todo(list_id, todo_id)
    flash('You successfully deleted a todo item', 'success')
    
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/todos/<todo_id>/update", methods=["POST"])
def update_todo(list_id, todo_id):
    is_completed = request.form.get('item_status') is not None 
    g.storage.update_todo_status(list_id, todo_id, is_completed)
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/complete_all", methods=["POST"])
def complete_all(list_id):
    g.storage.complete_all_todos(list_id)
    return redirect(url_for('show_list', list_id=list_id))

if __name__ == "__main__":
    app.run(debug=True, port=5003)