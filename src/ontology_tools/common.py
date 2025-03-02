"""
This module contains common classes and functions used by the ontology tools."""

from typing import NamedTuple


# defined a named tuple called Code with three fields: system, code, and display
class Code(NamedTuple):
    """Data structure to represent a code from a coding system."""

    system: str
    code: str
    display: str | None = None

    def __str__(self) -> str:
        return f"{self.system} {self.code}{f' {self.display}' if self.display else ''}"
