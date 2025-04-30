import enum


class Isolation(str, enum.Enum):
    autocommit = "AUTOCOMMIT"
    read_committed = "READ COMMITTED"
    read_uncommitted = "READ UNCOMMITTED"
    repeatable_read = "REPEATABLE READ"
    serializable = "SERIALIZABLE"
