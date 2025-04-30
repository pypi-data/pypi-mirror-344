import typing

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

Table = typing.TypeVar("Table", bound=Base)


__all__ = ["Table", "Base"]
