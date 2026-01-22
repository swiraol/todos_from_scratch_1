def error_for_list_title(title, all_lists):
    if not 1 <= len(title) <= 100:
        return "List name must be between 1 and 100 characters."
    
    if any(lst['title'] == title for lst in all_lists):
        return "List name must be unique"

    return None
