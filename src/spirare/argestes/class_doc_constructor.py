#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocConstructor

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from xml.etree.ElementTree import Element

from .doc_base import MethodReturnBase, ModelCollection, DocParameters, JsonBase, GodotBase


class ClassDocConstructor(MethodReturnBase,JsonBase, GodotBase):
    """
    Class DocConstructor

    :param name:  Name of the constructor
    :param description:  Description of the constructor (default None)
    :param parameters:  Parameters for the constructor (default None)
    """
    __slots__ = ()

    def __init__(self, name:str, description:str = None,qualifiers:str=None, parameters: DocParameters = None):
        MethodReturnBase.__init__(self, name=name, description=description,qualifiers=qualifiers, parameters=parameters)


class DocConstructors(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocConstructor, initlist)

    def new(self, **kwargs) -> ClassDocConstructor:
        constructor = ClassDocConstructor(**kwargs)
        self.append(constructor)
        return constructor

    def to_dict(self) -> dict:
        result = dict()
        result['constructors'] = []
        for constructor in self.data:
            result['constructors'].append(constructor.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocConstructor, json_str)

    @classmethod
    def from_xml(cls, element:Element):
        initial_list = [ClassDocConstructor.from_xml(e) for e in element]
        return cls(initial_list)