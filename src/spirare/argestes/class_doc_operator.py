#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocOperator

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import xml
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et

from . import ClassDocReturn
from .doc_base import MethodReturnBase, ClassDocParameter, ModelCollection, DocParameters, \
    DocDescription, Zucaritas


class ClassDocOperator(MethodReturnBase,Zucaritas):
    """
    This class represents a model of the class doc's operator element
    
    :param str name: The value of the name attribute for the operator element.
    :param DocDescription description: The value of the description element for the operator element.
    :param str qualifiers: The value of the qualifiers attribute for the operator element.
    :param DocParameters parameters: The value of the parameters element for the operator element.
    :param ClassDocReturn return_value: The value of the return_value element for the operator element.

    "What we've got here is failure to communicate"
    """
    __slots__ = ()

    def __init__(self, name:str, description:DocDescription=DocDescription(),qualifiers:str=None ,
                 return_value: ClassDocReturn = None,parameters: DocParameters = None):
        MethodReturnBase.__init__(self, name=name, description=description,qualifiers=qualifiers,
                                  parameters=parameters,return_value=return_value)


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        base_element = self._to_xml()
        base_element.tag = 'operator'
        return base_element

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


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        element = Et.Element('operators')
        for operator in self.data:
          element.append(operator.to_xml_doc())
        return element

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocOperator, json_str)

    @classmethod
    def from_xml(cls, element: xml.etree.ElementTree.Element):
        initial_list = [ClassDocOperator.from_xml(e) for e in element]
        return cls(initial_list)