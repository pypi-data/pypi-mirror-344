from .exceptions import InvalidPathError

def validate_path(path, separator='.'):
    """
    Validate if a given path is properly formatted.
    :param path: The path to validate.
    :param separator: The separator used in the path.
    :raises InvalidPathError: If the path is invalid.
    """
    try:
        check = True
        if not isinstance(path, str):
            check = False
            raise InvalidPathError("Path must be a string.")
        
        # Check if the path contains only valid characters
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789[]_")
        valid_chars.add(separator)
        for char in path:
            if char not in valid_chars:
                check = False
                raise InvalidPathError(f"Invalid character '{char}' in path.")

        # Ensure brackets are properly closed if present
        if '[' in path or ']' in path:
            if path.count('[') != path.count(']'):
                check = False
                raise InvalidPathError("Mismatched brackets in path.")
        return check
    except Exception as e:
        print(e)

def format_path(path, separator='.'):
    """
    Format a path for better readability.
    :param path: The path to format.
    :param separator: The separator used in the path.
    :return: A formatted version of the path.
    """
    try:
        if not isinstance(path, str):
            raise InvalidPathError("Path must be a string.")
        
        # Replace separators with a more readable format if needed
        return path.replace(separator, " -> ")
    except Exception as e:
        print(e)


def flatten_json(data, parent_key='', separator='.'):
    """
    Flatten a nested JSON structure into a single-level dictionary.
    :param data: The JSON data (dict or list).
    :param parent_key: The accumulated key path.
    :param separator: The separator to join keys.
    :return: A flattened dictionary.
    """
    try:
        items = {}
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                items.update(flatten_json(value, new_key, separator))
        elif isinstance(data, list):
            for index, value in enumerate(data):
                new_key = f"{parent_key}[{index}]"
                items.update(flatten_json(value, new_key, separator))
        else:
            items[parent_key] = data
        return items
    except Exception as e:
        print(e)
