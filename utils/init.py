def requires_arguments(func):
    """Returns True if the function takes arguments, False otherwise.

    Args:
        func: The function to check.

    Returns:
        True if the function takes arguments, False otherwise.
    """
    return func.__code__.co_argcount > 0


def init(definition):
    if not requires_arguments(definition):
        return definition()
    
    def wrapper(*args, **kwargs):
        return definition(*args, **kwargs)
    
    return wrapper