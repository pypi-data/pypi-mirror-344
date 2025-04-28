from enum import Enum


class MountCollaboratorBodyColumnsItemType(str, Enum):
    DOUBLE = "DOUBLE"
    INTEGER = "INTEGER"
    VARCHAR = "VARCHAR"

    def __str__(self) -> str:
        return str(self.value)
