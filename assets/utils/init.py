"""
copyright 2025 miuruwa
"""

from .require_args import requires_arguments


def init(definition):
    """
    Auto init method
    """

    if not requires_arguments(definition):
        return definition()

    return definition
