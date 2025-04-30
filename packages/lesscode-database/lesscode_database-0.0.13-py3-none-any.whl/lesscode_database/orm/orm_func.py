from typing import Union

from lesscode_database.orm.orm_typing import BaseColumnType


class OrmFunc:
    def __init__(self, func_name: str, alias: str = None, **kwargs):
        self.func_name = func_name
        self.alias = alias
        self.kwargs = kwargs or dict()

    def _name(self):
        return self.alias or str(self)

    def __repr__(self):
        if self.func_name in ["sum", "argv", "min", "max"]:
            column = self.kwargs.get("column")
            if column is None:
                return f"{self.func_name}()"
            else:
                if isinstance(column, BaseColumnType):
                    return f"{self.func_name}({column._name}) as {self.alias}" if self.alias else f"{self.func_name}({column._name})"
                else:
                    return f"{self.func_name}({repr(column)}) as {self.alias}" if self.alias else f"{self.func_name}({repr(column)})"
        else:
            return f"{self.func_name}({self.kwargs})"

    def __str__(self):
        return self.__repr__()


def func_sum(column: Union[BaseColumnType, int, float], alias=None):
    return OrmFunc(func_name="sum", column=column, alias=alias)


def func_min(column: Union[BaseColumnType, int, float], alias=None):
    return OrmFunc(func_name="min", column=column, alias=alias)


def func_max(column: Union[BaseColumnType, int, float], alias=None):
    return OrmFunc(func_name="max", column=column, alias=alias)


def func_argv(column: Union[BaseColumnType, int, float], alias=None):
    return OrmFunc(func_name="argv", column=column, alias=alias)
