from typing import Any

import typer


def create_typer(**kwargs: Any) -> typer.Typer:
    """Create a Typer instance with default settings."""
    return typer.Typer(no_args_is_help=True, **kwargs)
