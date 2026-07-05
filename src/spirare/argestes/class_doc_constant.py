#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocConstant

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et

from .doc_base import ConstantMemberBase, ModelCollection, Zucaritas


class ClassDocConstant(ConstantMemberBase,Zucaritas):
    """
    This class represents a model of the godot docs constant element
    
    :param str enum: The value of the enum attribute for the constant element.
    :param bool is_bitfield: The value of the is_bitfield attribute for the constant element.
    :param str name: The value of the name attribute for the constant element.
    :param str text: The value of the text attribute for the constant element.
    :param bool is_deprecated: The value of the is_deprecated attribute for the constant element.
    :param bool is_experimental: The value of the is_experimental attribute for the constant element.
    :param str deprecated: The value of the deprecated attribute for the constant element.
    :param str experimental: The value of the experimental attribute for the constant element.
    :param str keywords: The value of the keywords attribute for the constant element.
    :param str value: The value of the value attribute for the constant element.

    "Gentlemen, you can't fight in here!  This is the War Room!"
    """
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
        """
       Returns a dictionary of the values for this constant element model instance.

       :return: a dictionary of values for this constant model instance.
       """
        result = super().to_dict()
        result['value'] = self.value
        return result

    def to_xml_doc(self)->Element:
        base_element = self._to_xml()
        base_element.tag = 'constant'
        return base_element

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


    def to_xml_doc(self)->Element:
        element = Et.Element('constants')
        for constant in self.data:
          element.append(constant.to_xml_doc())
        return element

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocConstant, json_str)

    @classmethod
    def from_xml(cls, element:Element):
        initial_list = [ClassDocConstant.from_xml(e) for e in element]
        return cls(initial_list)