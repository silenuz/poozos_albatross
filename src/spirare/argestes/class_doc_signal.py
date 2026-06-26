#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocSignal

@Author: Phosphor (horuuendillus@gmail.com)
"""
from xml.etree import ElementTree as Et
from xml.etree.ElementTree import Element

from argestes.doc_base import MethodBase, ClassDocParameter, JsonBase, ModelCollection, GodotBase, DocParameters


class ClassDocSignal(MethodBase,JsonBase,GodotBase):
    __slots__ = ('is_deprecated', 'deprecated','is_experimental','experimental')
    is_deprecated: bool
    deprecated: str
    is_experimental: bool
    experimental: str

    def __init__(self,name:str,description:str=None, parameters:DocParameters=None,
                 is_deprecated: bool=None, deprecated: str = None, is_experimental: bool=None,
                 experimental: str=None) -> None:
        super().__init__(name=name,description=description,parameters=parameters)
        self.is_deprecated = is_deprecated
        self.deprecated = deprecated
        self.is_experimental = is_experimental
        self.experimental = experimental

    def to_dict(self) -> dict:
        result = super().to_dict()
        if self.is_deprecated is not None:
            result['is_deprecated'] = self.is_deprecated
        if self.deprecated is not None:
            result['deprecated'] = self.deprecated
        if self.is_experimental is not None:
            result['is_experimental'] = self.is_experimental
        if self.experimental is not None:
            result['experimental'] = self.experimental
        return result

class DocSignals(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocSignal, initlist)

    def new(self, **kwargs) -> ClassDocSignal:
        signal = ClassDocSignal(**kwargs)
        self.append(signal)
        return signal

    def to_dict(self) -> dict:
        result = dict()
        result['signals'] = []
        for signal in self.data:
            result['signals'].append(signal.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocSignal, json_str)

    @classmethod
    def from_xml(cls, element:Element):
        initial_list = [ClassDocSignal.from_xml(e) for e in element]
        return cls(initial_list)