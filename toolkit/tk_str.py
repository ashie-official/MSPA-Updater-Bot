def plural(object_qty, object_singular: str, object_plural: str = "", include_qty = True) -> str:
    result = f"{object_qty} " if include_qty else ""
    
    if object_qty == 1:
        return f"{result}{object_singular}"
    elif object_plural:
        return f"{result}{object_plural}"
    else:
        return f"{result}{object_singular}s"

def escape_format(my_str: str) -> str:
    result = my_str
    special_characters = '*_~`@#|-[]()>'
    for char in special_characters:
        result = result.replace(char,"\\" + char)
    return result