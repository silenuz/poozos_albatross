#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocConstant

@Author: Phosphor (horuuendillus@gmail.com)
"""
from xml.etree.ElementTree import Element

from argestes.doc_base import ConstantMemberBase, JsonBase, ModelCollection, GodotBase


class ClassDocConstant(ConstantMemberBase,JsonBase, GodotBase):
    __slots__ = 'value'
    value: str

    def __init__(self, name:str, value: str = None,text:str = None,enum:str = None, is_bitfield:bool = None,
                 keywords: str = None,is_deprecated:bool=None,is_experimental:bool=None,
                 deprecated: str = None, experimental: str = None):

        super().__init__(name=name,text=text,enum=enum,is_bitfield=is_bitfield,keywords=keywords,
                         is_deprecated=is_deprecated,is_experimental=is_experimental,deprecated=deprecated,
                         experimental=experimental)
        self.value = value

    def to_dict(self):
        result = super().to_dict()
        result['value'] = self.value
        return result

class DocConstants(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocConstant, initlist)

    def new(self, **kwargs) -> ClassDocConstant:
        constant = ClassDocConstant(**kwargs)
        self.append(constant)
        return constant

    def to_dict(self) -> dict:
        result = dict()
        result['constants'] = []
        for constant in self.data:
            result['constants'].append(constant.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocConstant, json_str)

    @classmethod
    def from_xml(cls, element:Element):
        initial_list = [ClassDocConstant.from_xml(e) for e in element]
        return cls(initial_list)