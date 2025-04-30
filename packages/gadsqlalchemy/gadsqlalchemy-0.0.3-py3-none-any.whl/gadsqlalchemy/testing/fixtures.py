import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


@pytest.fixture(scope="package", autouse=True)
def engine(dsn) -> AsyncEngine:
    return create_async_engine(dsn, echo=False)


@pytest.fixture(scope="package", autouse=True)
def sessionmaker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="package", autouse=True)
async def scopesession(engine, sessionmaker):
    async with sessionmaker() as _session:
        async with _session.begin():
            try:
                yield _session
            finally:
                await _session.rollback()
    await engine.dispose()


@pytest.fixture(scope="package", autouse=True)
def factories(scopesession, tables):
    for model in tables:
        model._meta.sqlalchemy_session = scopesession
    yield


@pytest.fixture(scope="function")
async def session(scopesession):
    async with scopesession.begin_nested() as _transaction:
        try:
            yield scopesession
        finally:
            await _transaction.rollback()
