import datetime
import time
from typing import Optional, Union, Any
from decimal import Decimal as _Decimal


class SubSelect:
    def __init__(self, sql: str, alias: str):
        self.sql = sql
        self.alias = alias


class BaseColumnType:

    def __init__(self, name: Optional[str], type_: Optional[Any],
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True,
                 primary_key: Optional[bool] = False,
                 alias: Optional[str] = None,
                 is_symbol: Optional[bool] = False, symbol="`",
                 comment=""):
        super(BaseColumnType, self).__init__()
        self.name = name or self.__class__.__name__.lower()
        self.name = f"{symbol}{self.name}{symbol}" if is_symbol else self.name
        self.alias = alias or self.name
        self.type_ = type_
        self.default = default
        self.index = index
        self.unique = unique
        self.nullable = nullable
        self.primary_key = primary_key
        self.comment = comment

    def _check_value(self, value):
        if not isinstance(value, self.type_):
            raise Exception(f"{value} is not {self.type_} type")

    def __eq__(self, other):
        # 返回格式化的字符串
        if not issubclass(other.__class__, BaseColumnType):
            return f"{self._name}={other}"
        else:
            return f"{self._name}={other._name}"

    def __ge__(self, other):
        # 返回格式化的字符串
        return f"{self._name}>={other._name}"

    def __gt__(self, other):
        # 返回格式化的字符串
        return f"{self._name}>{other._name}"

    def __le__(self, other):
        # 返回格式化的字符串
        return f"{self._name}<={other._name}"

    def __lt__(self, other):
        # 返回格式化的字符串
        return f"{self._name}<{other._name}"

    def __ne__(self, other):
        # 返回格式化的字符串
        return f"{self._name}!={other._name}"

    @property
    def _name(self):
        _table_name = self.owner.__table_name__ if hasattr(self, "owner") else ""
        return f"{_table_name}.{self.name}"

    def in_(self, value: Union[list, tuple, SubSelect]):
        if isinstance(value, SubSelect):
            return f"{self._name} in ({value.sql})"
        else:
            return f"{self._name} in {repr(value)}"

    def not_in(self, value: Union[list, tuple, SubSelect]):
        if isinstance(value, SubSelect):
            return f"{self._name} not in ({value.sql})"
        else:
            return f"{self._name} not in {repr(value)}"

    def like(self, value: str):
        return f"{self._name} like {repr(value)}"

    def not_like(self, value: str):
        return f"{self._name} not like {repr(value)}"

    def is_null(self, value="null"):
        return f"{self._name} is {value}"

    def is_not_null(self, value="null"):
        return f"{self._name} is not {value}"

    def desc(self):
        return f"{self._name} desc"

    def asc(self):
        return f"{self._name} asc"

    def alias(self, name):
        self.alias = name


class BaseColumnTypeAlias:
    def __init__(self, column_type, alias):
        self.column_type = column_type
        self.alias = alias

    @property
    def _name(self):
        return f"{self.column_type._name} as {self.alias}"


class TinyInt(BaseColumnType):

    def __init__(self, name: Optional[str], type_: Optional[Any] = int,
                 default: Optional[Any] = None,
                 nullable: Optional[bool] = True,
                 comment=""):
        if not issubclass(type_, int):
            raise Exception("type_ must be int")
        super().__init__(name=name, type_=type_, default=default, nullable=nullable,
                         comment=comment)


class SmallInt(BaseColumnType):

    def __init__(self, name: Optional[str], type_: Optional[Any] = int,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, int):
            raise Exception("type_ must be int")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class MediumInt(BaseColumnType):

    def __init__(self, name: Optional[str], type_: Optional[Any] = int,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, int):
            raise Exception("type_ must be int")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Int(BaseColumnType):

    def __init__(self, name: Optional[str], type_: Optional[Any] = int,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment="", autoincrement: bool = False):
        if not issubclass(type_, int):
            raise Exception("type_ must be int")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)
        self.autoincrement = autoincrement


class BigInt(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = int,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment="", autoincrement: bool = False):
        if not issubclass(type_, int):
            raise Exception("type_ must be int")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)
        self.autoincrement = autoincrement


class Decimal(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = _Decimal,
                 precision: int = 10, scale: int = 2,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, _Decimal):
            raise Exception("type_ must be decimal")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)
        self.precision = precision
        self.scale = scale


class Float(Decimal):
    def __init__(self, name: Optional[str], type_: Optional[Any] = float,
                 precision: int = 10, scale: int = 2,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, int):
            raise Exception("type_ must be float")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)
        self.precision = precision
        self.scale = scale


class Double(Decimal):
    def __init__(self, name: Optional[str], type_: Optional[Any] = float,
                 precision: int = 10, scale: int = 2,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, int):
            raise Exception("type_ must be float")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)
        self.precision = precision
        self.scale = scale


class Numeric(Decimal):
    def __init__(self, name: Optional[str], type_: Optional[Any] = _Decimal,
                 precision: int = 10, scale: int = 2,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, _Decimal):
            raise Exception("type_ must be decimal")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)
        self.precision = precision
        self.scale = scale


class Real(Decimal):
    def __init__(self, name: Optional[str], type_: Optional[Any] = float,
                 precision: int = 10, scale: int = 2,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, int):
            raise Exception("type_ must be float")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)
        self.precision = precision
        self.scale = scale


class Date(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = datetime.date,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, datetime.date):
            raise Exception("type_ must be Date")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class DateTime(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = datetime.datetime,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, datetime.datetime):
            raise Exception("type_ must be DateTime")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class TimeStamp(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = datetime.datetime,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, datetime.datetime):
            raise Exception("type_ must be TimeStamp")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Time(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = datetime.time,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, datetime.time):
            raise Exception("type_ must be Time")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Year(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = int,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, int):
            raise Exception("type_ must be Year")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Char(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = str,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, str):
            raise Exception("type_ must be Char")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Text(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = str,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, str):
            raise Exception("type_ must be Text")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Varchar(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = str,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, str):
            raise Exception("type_ must be Text")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Binary(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = bytes,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, bytes):
            raise Exception("type_ must be Binary")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Varbinary(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = bytes,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, bytes):
            raise Exception("type_ must be Varbinary")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Bolb(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = bytes,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, bytes):
            raise Exception("type_ must be Bolb")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Boolean(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = bool,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, bool):
            raise Exception("type_ must be Boolean")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class Bool(BaseColumnType):
    def __init__(self, name: Optional[str], type_: Optional[Any] = bool,
                 default: Optional[Any] = None, index: Optional[bool] = None,
                 unique: Optional[bool] = None, nullable: Optional[bool] = True, primary_key: Optional[bool] = False,
                 comment=""):
        if not issubclass(type_, bool):
            raise Exception("type_ must be Boolean")
        super().__init__(name=name, type_=type_, default=default, index=index, unique=unique, nullable=nullable,
                         primary_key=primary_key, comment=comment)


class ResultColumnType:
    def __init__(self, name: str = None, type_: Any = None, column: BaseColumnType = None, alias: str = None,
                 value: Any = None):
        self.name = name or alias or column.name
        self.type_ = type_ or column.type_
        self.column = column
        self.alias = alias
        self.value = value


class ResultRow:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Result:
    def __init__(self, rows: list):
        self.rows = rows

    def to(self):
        result = []
        for row in self.rows:
            _d = vars(row)
            result.append(_d)
