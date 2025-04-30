from typing import Union

from lesscode_database.ds_helper import DsHelper
from lesscode_database.orm.orm_func import OrmFunc
from lesscode_database.orm.orm_model import BaseModel
from lesscode_database.orm.orm_typing import BaseColumnType, BaseColumnTypeAlias, SubSelect, Int, TinyInt, SmallInt, \
    MediumInt


class Select:
    def __init__(self, *args):
        self._tables = []
        self._column_tables = []
        self._columns = []
        self._origin_column_map = dict()
        self._joins = []
        self._conditions = []
        self._group_by = []
        self._having = []
        self._order_by = []
        self._limit = []
        self._connect_name = None
        for arg in args:
            if isinstance(arg, BaseColumnType):
                if hasattr(arg, "owner"):
                    if not self._connect_name:
                        self._connect_name = arg.owner.__bind_key__ if hasattr(arg.owner, '__bind_key__') else None
                    _table_name = arg.owner.__table_name__ if hasattr(arg.owner, "__table_name__") else ""
                    if _table_name and _table_name not in self._tables:
                        self._column_tables.append(_table_name)
                self._columns.append(arg._name)
                self._origin_column_map = {arg._name: arg}

            elif isinstance(arg, BaseColumnTypeAlias):
                _ct = arg.column_type
                if isinstance(_ct, BaseColumnType):
                    if hasattr(_ct, "owner"):
                        _table_name = _ct.owner.__table_name__ if hasattr(_ct, "__table_name__") else ""
                        if _table_name and _table_name not in self._column_tables:
                            self._column_tables.append(_table_name)
                        if not self._connect_name:
                            self._connect_name = _ct.owner.__bind_key__ if hasattr(_ct.owner, '__bind_key__') else None
                self._origin_column_map = {arg.alias: arg}
                self._columns.append(arg._name)

            elif isinstance(arg, OrmFunc):
                self._columns.append(str(arg))
                self._origin_column_map = {arg._name: arg}

            elif issubclass(arg, BaseModel):
                if hasattr(arg, "__table_name__"):
                    _table_name = arg.__table_name__
                    if _table_name and _table_name not in self._column_tables:
                        self._column_tables.append(_table_name)
                if not self._connect_name:
                    if hasattr(arg, "__bind_key__"):
                        self._connect_name = arg.__bind_key__
                _attrs = vars(arg)
                for attr in _attrs:
                    if hasattr(arg, attr):
                        if isinstance(getattr(arg, attr), BaseColumnType):
                            self._origin_column_map = {getattr(arg, attr)._name: getattr(arg, attr)}
                            self._columns.append(getattr(arg, attr)._name)
            else:
                raise TypeError("args must be str or BaseColumnType")

    def select_from(self, model):
        if isinstance(model, list):
            for _model in model:
                if issubclass(_model, BaseModel):
                    if hasattr(_model, "__table_name__"):
                        if _model.__table_name__ not in self._tables:
                            self._tables.append(_model.__table_name__)
                    if not self._connect_name:
                        if hasattr(_model, "__bind_key__"):
                            self._connect_name = _model.__bind_key__
                else:
                    raise TypeError("model must be BaseModel")
        elif issubclass(model, BaseModel):
            if hasattr(model, "__table_name__"):
                if model.__table_name__ not in self._tables:
                    self._tables.append(model.__table_name__)
            if not self._connect_name:
                if hasattr(model, "__bind_key__"):
                    self._connect_name = model.__bind_key__
        else:
            raise TypeError("model must be BaseModel")
        return self

    def join(self, model, relation_list: list, how="left join"):
        if not issubclass(model, BaseModel):
            raise TypeError("model must be BaseModel")
        self._joins.append(f"{how} {model.__table_name__} ON {' and '.join(relation_list)}")
        return self

    def where(self, *args):
        self._conditions = [arg for arg in args]
        return self

    def group_by(self, *args):
        self._group_by = [arg for arg in args]
        return self

    def having(self, *args):
        self._having = [arg for arg in args]
        return self

    def order_by(self, *args):
        self._order_by = [arg for arg in args]
        return self

    def limit(self, offset=0, num=10):
        self._limit = [offset, num]
        return self

    def sub(self, alias: str = None):
        return SubSelect(sql=self._sql(), alias=alias)

    def _sql(self):
        sql = f"select {','.join(self._columns)}"
        if self._tables:
            sql += f" from {' , '.join(self._tables)}"
        else:
            if self._column_tables:
                sql += f" from {' , '.join(self._column_tables)}"
        if self._joins:
            sql += " " + " ".join(self._joins)
        if self._conditions:
            sql += " where " + " and ".join(self._conditions)

        if self._group_by:
            sql += " group by " + " , ".join(self._group_by)
        if self._having:
            sql += " having " + " and ".join(self._having)
        if self._order_by:
            sql += " order by " + " , ".join(self._order_by)
        if self._limit:
            sql += f" limit {self._limit[0]},{self._limit[1]}"
        return sql

    def __repr__(self):
        return self._sql()

    def __str__(self) -> str:
        return self.__repr__()


class Update:
    def __init__(self, model):
        self._table = ""
        self._conditions = []
        self._connect_name = ""
        self.update_values = {}
        if issubclass(model, BaseModel):
            self._table = model.__table_name__
            self._connect_name = model.__bind_key__
        else:
            raise TypeError("model must be BaseModel")

    def where(self, *args):
        self._conditions = [arg for arg in args]
        return self

    def values(self, **kwargs):
        self.update_values = kwargs

    def _sql(self):
        sql = f"update {self._table} set "
        update_column_sql = ','.join([f"{k}={v}" for k, v in self.update_values.items()])
        sql += update_column_sql
        if self._conditions:
            sql += " where " + " and ".join(self._conditions)
        return sql


class Delete:
    def __init__(self, model):
        self._table = ""
        self._conditions = []
        self._connect_name = ""
        self.update_values = {}
        if issubclass(model, BaseModel):
            self._table = model.__table_name__
            self._connect_name = model.__bind_key__
        else:
            raise TypeError("model must be BaseModel")

    def where(self, *args):
        self._conditions = [arg for arg in args]
        return self

    def _sql(self):
        sql = f"delete from {self._table}"
        if self._conditions:
            sql += " where " + " and ".join(self._conditions)
        return sql


class Insert:
    def __init__(self, model):
        self._table = ""
        self._connect_name = ""
        self.insert_values = {}
        if issubclass(model, BaseModel):
            self._table = model.__table_name__
            self._connect_name = model.__bind_key__
        else:
            raise TypeError("model must be BaseModel")

    def values(self, data: Union[list, dict]):
        self.insert_values = data

    def _sql(self):
        sql = f"insert into {self._table} "
        insert_column_list = []
        insert_value_list = []
        if isinstance(self.insert_values, list):
            one = self.insert_values[0]
            insert_column_list = list(one.keys())
            for _ in self.insert_values:
                _insert_value_list = []
                for k in insert_column_list:
                    if _[k] is None:
                        _insert_value_list.append("null")
                    else:
                        _insert_value_list.append(_[k])
                insert_value_list.append(f"""({','.join(_insert_value_list)})""")
        else:
            _insert_value_list = []
            for k, v in self.insert_values.items():
                if v is None:
                    insert_column_list.append(k)
                    _insert_value_list.append("null")
                else:
                    insert_column_list.append(k)
                    _insert_value_list.append(v)
            insert_value_list.append(f"""({','.join(_insert_value_list)})""")
        sql += f"({','.join(insert_column_list)}) values ({','.join(insert_value_list)})"
        return sql


class Exec:
    __connect_name__ = None

    def __init__(self, connect_name: str = None):
        self.__connect_name__ = connect_name or self.__connect_name__
        self._sql = ""
        self._result = None
        self._sql_type = ""

    def execute(self, statement: Union[Select, Update, Delete, Insert, str]):
        if not self.__connect_name__ and not isinstance(statement, str):
            self.__connect_name__ = statement._connect_name
        if isinstance(statement, str):
            self._sql = statement
            return self
        else:
            self._sql = statement._sql()
            return self

    def all(self):
        self._sql_type = "all"
        self._result = DsHelper(self.__connect_name__).exec_(self._sql_type, self._sql)
        return self._result

    async def async_all(self):
        self._sql_type = "all"
        self._result = await DsHelper(self.__connect_name__).async_exec_(self._sql_type, self._sql)
        return self._result

    def first(self):
        self._sql_type = "first"
        self._result = DsHelper(self.__connect_name__).exec_(self._sql_type, self._sql)
        return self._result

    async def async_first(self):
        self._sql_type = "first"
        self._result = await DsHelper(self.__connect_name__).async_exec_(self._sql_type, self._sql)
        return self._result

    def update(self):
        self._sql_type = "update"
        self._result = DsHelper(self.__connect_name__).exec_(self._sql_type, self._sql)
        return self._result

    async def async_update(self):
        self._sql_type = "update"
        self._result = await DsHelper(self.__connect_name__).async_exec_(self._sql_type, self._sql)
        return self._result

    def delete(self):
        self._sql_type = "delete"
        self._result = DsHelper(self.__connect_name__).exec_(self._sql_type, self._sql)
        return self._result

    async def async_delete(self):
        self._sql_type = "delete"
        self._result = await DsHelper(self.__connect_name__).async_exec_(self._sql_type, self._sql)
        return self._result

    def insert(self):
        self._sql_type = "insert"
        self._result = DsHelper(self.__connect_name__).exec_(self._sql_type, self._sql)
        return self._result

    async def async_insert(self):
        self._sql_type = "insert"
        self._result = await DsHelper(self.__connect_name__).async_exec_(self._sql_type, self._sql)
        return self._result


class TestModel(BaseModel):
    __table_name__ = 'test_table'
    __table_args__ = {'comment': '测试表'}
    __bind_key__ = 'test_db'
    id = Int('id', int, primary_key=True, autoincrement=True)
    name = TinyInt('name', int)
    age = SmallInt('age', int)
    height = MediumInt('height', int)


a = Select(TestModel.id.alias("a"))
b = a.join(TestModel, [TestModel.id == TestModel.id]).where(TestModel.id == 1)

print(Exec().execute(b))
