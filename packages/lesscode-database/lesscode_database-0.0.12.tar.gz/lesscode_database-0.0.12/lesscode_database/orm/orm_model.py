from lesscode_database.orm.orm_typing import BaseColumnType


class Meta(type):
    def __new__(cls, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, BaseColumnType):
                attr_value.name = attr_name
                attr_value.owner = None
        new_cls = super().__new__(cls, name, bases, namespace)
        for attr_value in namespace.values():
            if isinstance(attr_value, BaseColumnType):
                attr_value.owner = new_cls
                attr_value.connect_name = new_cls.__bind_key__ if hasattr(new_cls, '__bind_key__') else None
        return new_cls


class BaseModel(metaclass=Meta):
    __table_name__ = 'base'
    __table_args__ = {}
    __bind_key__ = 'default'
