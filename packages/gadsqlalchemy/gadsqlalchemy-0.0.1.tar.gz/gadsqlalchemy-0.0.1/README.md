<p align="center">
  <a href="https://github.com/AlexDemure/gadsqlalchemy">
    <a href="https://ibb.co/QFMLpQhC"><img src="https://i.ibb.co/Lz1mYRBJ/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  Wrapper around SQLAlchemy AsyncSession with built-in query execution profiling and connection context management.
</p>

---

### Installation

```
pip install gadsqlalchemy
```

### Usage

```python
from gadsqlalchemy import Sqlalchemy, Base


alchemy = Sqlalchemy("postgresql+asyncpg://postgres:postgres@localhost:5432/db")


class Table(Base):
    ...


class Service:

    @classmethod
    async def get(cls):
        async with alchemy.connect() as session:
            ...

    @classmethod
    async def create(cls,):
        async with alchemy.connect(transaction=True) as session:
           ...
```
