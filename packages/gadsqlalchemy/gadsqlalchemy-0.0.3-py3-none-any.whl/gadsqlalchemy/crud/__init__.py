import datetime

from gadsqlalchemy.exceptions import ObjectNotFoundError
from gadsqlalchemy.tables import Table
from sqlalchemy import BinaryExpression
from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select


async def fetchcount(session: AsyncSession, query: Select) -> int:
    return (await session.execute(select(func.count()).select_from(query.subquery()))).scalars().one()


async def fetchone(session: AsyncSession, query: Select) -> Table:
    try:
        return (await session.execute(query)).scalars().one()
    except NoResultFound:
        raise ObjectNotFoundError


async def fetchall(session: AsyncSession, query: Select) -> list[Table]:
    return (await session.execute(query)).scalars().all()  # type:ignore


class CRUD:
    table: Table

    @classmethod
    def filters(cls, fields: dict) -> list[BinaryExpression]:
        expressions = []

        for key in fields.keys():
            if fields[key] is not None:
                if isinstance(fields[key], list):
                    expressions.append(getattr(cls.table, key).in_(fields[key]))
                elif isinstance(fields[key], datetime.date):
                    expressions.append(func.DATE(getattr(cls.table, key)) == fields[key])
                else:
                    expressions.append(getattr(cls.table, key) == fields[key])

        return expressions

    @classmethod
    async def id(cls, session: AsyncSession) -> int:
        sequence = f"{cls.table.__tablename__}_id_seq"
        query = text("SELECT nextval(:sequence)")
        return (await session.execute(query, {"sequence": sequence})).scalar()

    @classmethod
    async def one(cls, session: AsyncSession, **kwargs) -> Table:
        query = select(cls.table).where(*cls.filters(kwargs))
        return await fetchone(session, query)

    @classmethod
    async def relations(cls, session: AsyncSession, **kwargs) -> Table:
        raise NotImplementedError

    @classmethod
    async def paginated(
        cls,
        session: AsyncSession,
        filters: dict,
        sorting: dict,
        pagination: dict,
    ) -> tuple[list[Table], int]:
        raise NotImplementedError

    @classmethod
    async def all(cls, session: AsyncSession, **kwargs) -> list[Table]:
        query = select(cls.table).where(*cls.filters(kwargs))
        return await fetchall(session, query)

    @classmethod
    async def count(cls, session: AsyncSession, **kwargs) -> int:
        query = select(cls.table).where(*cls.filters(kwargs))
        return await fetchcount(session, query)

    @classmethod
    async def exists(cls, session: AsyncSession, **kwargs) -> bool:
        query = exists().where(*cls.filters(kwargs)).select()
        return (await session.execute(query)).scalar()

    @classmethod
    async def create(cls, session: AsyncSession, row: dict) -> Table:
        columns = {k: v for k, v in row.items() if getattr(cls.table, k, None) is not None}
        instance = cls.table(**columns)
        session.add(instance)
        await session.flush()
        return instance

    @classmethod
    async def update(cls, session: AsyncSession, id: str | int, **kwargs) -> None:
        columns = {k: v for k, v in kwargs.items() if getattr(cls.table, k, None) is not None}
        query = update(cls.table).where(cls.table.id == id).values(**columns)
        await session.execute(query)
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, **kwargs) -> None:
        query = delete(cls.table).where(*cls.filters(kwargs))
        await session.execute(query)
        await session.flush()


__all__ = ["CRUD", "fetchone", "fetchall", "fetchcount"]
