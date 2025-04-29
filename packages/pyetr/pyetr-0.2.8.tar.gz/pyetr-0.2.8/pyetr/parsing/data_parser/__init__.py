from __future__ import annotations

__all__ = ["view_to_json", "json_to_view"]


import typing

import pyetr.parsing.data_parser.models as models
from pyetr.parsing.view_storage import ViewStorage

if typing.TYPE_CHECKING:
    from pyetr.view import View

from .model_to_view import model_to_view
from .view_to_model import view_to_model


def view_to_json(v: View) -> str:
    """
    Parses from View form to json form

    Args:
        v (View): The input view

    Returns:
        str: The output json
    """
    return view_to_model(v).model_dump_json()


def json_to_view(s: str) -> ViewStorage:
    """
    Parses from json form to View form

    Args:
        s (str): The json string

    Returns:
        ViewStorage: The parsed view
    """
    return model_to_view(models.View.model_validate_json(s))
