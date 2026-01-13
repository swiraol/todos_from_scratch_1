import psycopg2 
from psycopg2.extras import DictCursor 
from contextlib import contextmanager 

class DatabasePersistence:
    def __init__(self):
        pass
    
    @contextmanager
    def _database_connect(self):
        connection = psycopg2.connect(dbname="todos")
        try:
            with connection:
                yield connection 
        finally:
            connection.close()

    def all_lists(self):
        query = "SELECT * FROM lists"
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                all_lists = cursor.fetchall()
        
        return all_lists
    
    def create_list(self, title):
        query = "INSERT INTO lists (title) VALUES (%s)"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (title,))

    def find_list(self, list_id):
        query = "SELECT * FROM lists WHERE id = %s"

        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (list_id,))
                lst = cursor.fetchone()
                lst = dict(lst)
        
        todos = self.find_todos(list_id)
        lst['todos'] = todos

        return lst

    def edit_list(self):
        pass 

    def delete_list(self):
        pass 

    def create_todo(self, list_id, todo_title):
        query = "INSERT INTO todos (title, list_id) VALUES (%s, %s)"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (todo_title, list_id))

    def find_todos(self, list_id):
        query = "SELECT * FROM todos WHERE list_id = %s"

        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (list_id,))
                todos = cursor.fetchall()
                print(f"todos: {todos}")
                todos = [dict(todo) for todo in todos]
        
        return todos

    def update_todo_status(self):
        pass 

    def complete_all_todos(self):
        pass 

