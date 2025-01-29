"""
copyright 2025 miuruwa
"""

import inspect


def requires_arguments(definition):
    """Returns True if the function takes arguments, False otherwise.

    Args:
        definition: The function or class to check.

    Returns:
        True if the function takes arguments, False otherwise.
    """

    if inspect.isclass(definition):
        return definition.__init__.__code__.co_argcount > 1

    return definition.__code__.co_argcount > 0
