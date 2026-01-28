def error_for_title(title, all_lists, name):
    if not 1 <= len(title) <= 100:
        return f"{name} title must be between 1 and 100 characters."
    
    if any(lst['title'] == title for lst in all_lists):
        return f"{name} title must be unique"

    return None

# def sort_todos():
#     pass
