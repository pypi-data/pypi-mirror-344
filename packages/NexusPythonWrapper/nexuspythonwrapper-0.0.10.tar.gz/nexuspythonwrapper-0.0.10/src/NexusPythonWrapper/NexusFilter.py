import json
from typing import Self

class NexusFilter:
    filter_operators = {'and', 'or'}
    filter_methods = {'eq', 'lt', 'gt', 'le', 'ge'} # also supports; like, in, pa, ch - testing required
    
    def __init__(self, operator: str = 'and') -> None:
        self._where = []
        self._nested = []
        if operator and operator.lower() not in self.filter_operators:
            raise ValueError(f'Invalid filter operator: {operator}. Must use one of {self.filter_operators}')
        self.operator = operator.lower()

    def where(self, field: str, value: str | int | float, method: str = None, invert: bool = None) -> Self:
        nexus_filter = {
            'field': field,
            'value': value
        }

        if method:
            if method.lower() not in self.filter_methods:
                raise ValueError(f'Invalid filter method: {method}. Must use one of {self.filter_methods}')
            nexus_filter['method'] = method.lower()

        if invert:
            nexus_filter['not'] = invert

        self._where.append(nexus_filter)

        return self

    def nested(self, nexus_filter: 'NexusFilter') -> Self:
        self._nested.append(nexus_filter.build(raw=True))
        return self

    def and_(self) -> Self:
        self.operator = 'and'
        return self 

    def or_(self) -> Self:
        self.operator = 'or'
        return self 

    def build(self, raw: bool = False):
        nexus_filter = {
            'operator': self.operator
        }

        if self._where:
            nexus_filter['where'] = self._where

        if self._nested:
            nexus_filter['nested'] = self._nested

        return nexus_filter if raw else json.dumps(nexus_filter)


    def __str__(self) -> str:
        return self.build()
