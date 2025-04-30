# Copyright Amethyst Reese
# Licensed under the MIT license

"""asyncio bridge to the standard sqlcipher3 module"""

from sqlcipher3 import (  # pylint: disable=redefined-builtin
    DatabaseError,
    Error,
    IntegrityError,
    NotSupportedError,
    OperationalError,
    paramstyle,
    ProgrammingError,
    register_adapter,
    register_converter,
    Row,
    sqlite_version,
    sqlite_version_info,
    Warning,
)

from .core import connect, Connection, Cursor

__all__ = [
    "paramstyle",
    "register_adapter",
    "register_converter",
    "sqlite_version",
    "sqlite_version_info",
    "connect",
    "Connection",
    "Cursor",
    "Row",
    "Warning",
    "Error",
    "DatabaseError",
    "IntegrityError",
    "ProgrammingError",
    "OperationalError",
    "NotSupportedError",
]
