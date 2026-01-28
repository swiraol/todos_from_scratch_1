# setup project 
  # create app.py file and set up a basic Flask application
  # create schema.sql file to define the database schema for the lists and todos tables.
# persistence layer
  # Create a database_persistence.py file to handle all database interactions.
  # Define a DatabasePersistence class inside this file.
  # Implement methods for connecting to and querying the PostgreSQL database.
  # In app.py, use an @app.before_request hook to create an instance of your persistence class and store it on Flask's g object for access within your routes.
# Implement List Functionality (CRUD)
  # View all lists​: Create a route for /lists (GET) that queries for all lists and renders the lists.html template.
  # Create a list​: Create a route for /lists (POST) to process the form submission from the main page. Implement validation for the list name.
  # ​View a single list​: Create a route for /lists/<list_id> that displays a single list and its associated todos.
  # ​Edit a list​: Create routes for /lists/<list_id>/edit to display the edit form (GET) and process the submission (POST).
  # ​Delete a list​: Create a route for /lists/<list_id>/delete (POST) to remove a list.
# Implement Todo Functionality (CRUD)
  # ​Create a todo​: Create a route for /lists/<list_id>/todos (POST) that adds a new todo to a list. Implement validation for the todo name.
  # ​Delete a todo​: Create a route for /lists/<list_id>/todos/<todo_id>/delete (POST).
  # ​Toggle a todo's status​: Create a route for /lists/<list_id>/todos/<todo_id>/toggle (POST) to update its completion status.
  # ​Complete all todos​: Create a route for /lists/<list_id>/complete_all (POST) to mark all todos in a list as complete.
# Implement validations
  # Create a validation that checks for a list title error
  # Create a validation that checks for a todo title error
# Implement flash messages
  # After an action is completed (like creating a list, deleting a todo, etc.), the application should provide feedback to the user. 
# Refactoring
  # As discussed in the Removing Code Duplication assignment, the logic for finding a list or todo and handling a "not found" scenario is repeated. Refactor this logic into decorators (@require_list, @require_todo) to keep your routes clean.
# Sorting logic
  # The lists on the main page and the todos within each list page should be sorted. The required behavior is to display incomplete items before completed ones, with each group sorted alphabetically by title.
# Implement a layout template for shared page structure.
# Show the number of remaining todos for each list on the /lists page while conserving resources