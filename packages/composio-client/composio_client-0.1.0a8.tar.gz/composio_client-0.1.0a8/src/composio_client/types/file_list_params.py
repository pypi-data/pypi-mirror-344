# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["FileListParams"]


class FileListParams(TypedDict, total=False):
    action: str
    """Name of the action where this file belongs to."""

    app: str
    """Name of the app where this file belongs to."""
