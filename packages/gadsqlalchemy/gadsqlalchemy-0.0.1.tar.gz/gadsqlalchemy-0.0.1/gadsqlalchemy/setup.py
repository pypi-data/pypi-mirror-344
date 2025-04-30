import contextlib
import typing

from gadsqlalchemy import enums
from gadsqlalchemy import patches
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


class Sqlalchemy:
    def __init__(
        self,
        dsn: str,
        *,
        debug: bool = False,
        serializer: typing.Callable | None = None,
        isolation: enums.Isolation = enums.Isolation.read_committed,
    ) -> None:
        self.engine = create_async_engine(
            dsn,
            echo=debug,
            future=True,
            isolation_level=isolation,
            json_serializer=serializer,
        )
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _read(self) -> AsyncSession:
        async with self.sessionmaker() as session:
            patches.profiler(session)
            await session.connection(execution_options={"isolation_level": enums.Isolation.autocommit})
            yield session

    @contextlib.asynccontextmanager
    async def _write(self) -> AsyncSession:
        async with self.sessionmaker() as session:
            patches.profiler(session)
            try:
                async with session.begin():
                    yield session
            except Exception as e:
                await session.rollback()
                raise e

    @contextlib.asynccontextmanager
    async def connect(self, transaction: bool = False) -> AsyncSession:
        if transaction:
            async with self._write() as session:
                yield session
        else:
            async with self._read() as session:
                yield session
