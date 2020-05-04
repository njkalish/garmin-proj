from reprlib import recursive_repr

from sqlalchemy.ext.declarative import declarative_base

MyBase = declarative_base()


@recursive_repr()
def base_repr(self):
    keys = [k for k in self.__class__.__dict__ if not k.startswith('_')]
    values = [getattr(self, k) for k in keys]

    name = f'<{self.__class__.__name__}(\n'
    for key, value in zip(keys, values):
        name += f'\t{key}={value}\n'
    name += ')>'

    return name


MyBase.__repr__ = base_repr
