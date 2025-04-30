import logging

from gadsqlalchemy import contextmanagers
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable

logger = logging.getLogger("sqlalchemy.profiler")


def profiler(session: AsyncSession) -> None:
    execute = session.execute

    async def _execute(statement: Executable, *args, **kwargs) -> Result:
        with contextmanagers.timer() as timer:
            try:
                return await execute(statement, *args, **kwargs)
            finally:
                query = str(statement.compile(compile_kwargs={"literal_binds": True}))
                logger.info(query, extra={"elapsed": timer()})

    session.execute = _execute
