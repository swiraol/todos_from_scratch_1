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
    
    def create_list(self):
        pass 

    def view_list(self):
        pass 

    def edit_list(self):
        pass 

    def delete_list(self):
        pass 

    def create_todo(self):
        pass 

    def update_todo_status(self):
        pass 

    def complete_all_todos(self):
        pass 

