#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocOperator

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from xml.etree.ElementTree import Element

from .doc_base import MethodReturnBase, ClassDocParameter, ModelCollection, JsonBase, GodotBase, DocParameters, \
    DocDescription


class ClassDocOperator(MethodReturnBase,JsonBase,GodotBase):
    """
    Class DocOperator

    :param name:  Name of the operator
    :param description:  Description of the operator (default None)
    :param parameters:  Parameters for the operator (default None)
    """
    __slots__ = ()

    def __init__(self, name:str, description:DocDescription=DocDescription(),qualifiers:str=None ,parameters: DocParameters = None):
        MethodReturnBase.__init__(self, name=name, description=description,qualifiers=qualifiers, parameters=parameters)


class DocOperators(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocOperator, initlist)

    def new(self, **kwargs) -> ClassDocOperator:
        operator = ClassDocOperator(**kwargs)
        self.append(operator)
        return operator

    def to_dict(self) -> dict:
        result = dict()
        result['operators'] = []
        for method in self.data:
            result['operators'].append(method.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocOperator, json_str)

    @classmethod
    def from_xml(cls, element: Element):
        initial_list = [ClassDocOperator.from_xml(e) for e in element]
        return cls(initial_list)