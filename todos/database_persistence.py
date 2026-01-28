import psycopg2 
from psycopg2.extras import DictCursor 
from contextlib import contextmanager 
from werkzeug.exceptions import NotFound 

class DatabasePersistence:
    def __init__(self):
        self._setup_schema()
    
    def _setup_schema(self):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'lists';
                """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                                   CREATE TABLE lists (
                                        id serial PRIMARY KEY,
                                        title text NOT NULL UNIQUE
                                   );
                    """)
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'todos';
                """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        CREATE TABLE todos (
                                   id SERIAL PRIMARY KEY,
                                   title text NOT NULL,
                                   completed BOOLEAN NOT NULL,
                                   list_id INTEGER REFERENCES lists (id) ON DELETE CASCADE
                        );
                    """)

    @contextmanager
    def _database_connect(self):
        connection = psycopg2.connect(dbname="todos")
        try:
            with connection:
                yield connection 
        finally:
            connection.close()

    def all_lists(self):
        query = """SELECT l.id, l.title,
                          COUNT(t.id) as total_todos,
                          COUNT(CASE WHEN NOT t.completed THEN 1 END) as incomplete_todos
                   FROM lists l
                   LEFT JOIN todos t on l.id = t.list_id
                   GROUP BY l.id, l.title
                   ORDER BY l.title ASC
        """
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
                if lst is None:
                    raise NotFound(f"List with ID {list_id} not found.")
        lst = dict(lst)
        
        todos = self.find_todos(list_id)
        lst['todos'] = todos

        return lst

    def edit_list(self, list_id, title):
        query = "UPDATE lists SET title = %s WHERE id = %s"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (title, list_id))

    def delete_list(self, list_id):
        query = "DELETE FROM lists WHERE id = %s"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (list_id,))

    def create_todo(self, list_id, todo_title):
        query = "INSERT INTO todos (title, list_id) VALUES (%s, %s)"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (todo_title, list_id))

    def find_todos(self, list_id):
        query = "SELECT * FROM todos WHERE list_id = %s ORDER BY completed ASC, title ASC"

        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (list_id,))
                todos = cursor.fetchall()
                todos = [dict(todo) for todo in todos]
        return todos

    def get_todos_count(self, list_id):
        query = """
            SELECT COUNT(*) FROM todos WHERE list_id = %s
        """
        
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (list_id,))
                count = cursor.fetchone()
        
        return count[0]
    
    def get_incomplete_todos_count(self, list_id):
        query = """
            SELECT COUNT(*) FROM todos WHERE completed = False AND list_id = %s
        """

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (list_id,))
                count = cursor.fetchone()
        
        return count[0] 

    def delete_todo(self, list_id, todo_id):
        query = "DELETE FROM todos WHERE id = %s and list_id = %s"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (todo_id, list_id))

    def update_todo_status(self, list_id, todo_id, status):
        query = "UPDATE todos SET completed = %s WHERE id = %s and list_id = %s"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (status, todo_id, list_id))

    def complete_all_todos(self, list_id):
        query = "UPDATE todos SET completed = True WHERE list_id = %s"

        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (list_id,))

