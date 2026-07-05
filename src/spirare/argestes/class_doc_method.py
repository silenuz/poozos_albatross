#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocMethod

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et

from . import ClassDocReturn
from .class_doc_annotation import ClassDocAnnotation
from .doc_base import DocReturnErrorsList, ModelCollection, DocParameters, DocDescription, Zucaritas


class ClassDocMethod(ClassDocAnnotation,Zucaritas):
    """
    This class represents a model of the class doc's method element
    
    :param str name: The value of the name attribute for the method element.
    :param DocDescription description: The value of the description element for the method element.
    :param str qualifiers: The value of the qualifiers attribute for the method element.
    :param DocParameters parameters: The value of the parameters element for the method element.
    :param ClassDocReturn return_value: The value of the return_value element for the method element.
    :param str keywords: The value of the keywords attribute for the method element.
    :param DocReturnErrorsList returns_errors: The value of the returns_errors element for the method element.
    :param bool is_deprecated: The value of the is_deprecated attribute for the method element.
    :param bool is_experimental: The value of the is_experimental attribute for the method element.
    :param str deprecated: The value of the deprecated attribute for the method element.
    :param str experimental: The value of the experimental attribute for the method element.
    """
    __slots__ = ('returns_errors','is_deprecated','is_experimental','deprecated','experimental')
    returns_errors: DocReturnErrorsList
    is_deprecated: bool
    is_experimental: bool
    deprecated: str
    experimental: str

    def __init__(self, name: str, description: DocDescription=DocDescription(),qualifiers:str=None, parameters: DocParameters = None,
                 return_value: ClassDocReturn = None, returns_errors: DocReturnErrorsList = None,
                 keywords:str=None, is_deprecated: bool = None, is_experimental: bool = None,
                 deprecated:str = None, experimental:str = None):
        ClassDocAnnotation.__init__(self, name=name, description=description, qualifiers=qualifiers,parameters=parameters,return_value=return_value,keywords=keywords)
        self.returns_errors = returns_errors
        self.is_deprecated = is_deprecated
        self.is_experimental = is_experimental
        self.deprecated = deprecated
        self.experimental = experimental

    def to_dict(self) -> dict:
        values = super().to_dict()
        if self.returns_errors is not None:
            values.update(self.returns_errors.to_dict())
        if self.is_deprecated is not None:
            values['is_deprecated'] = self.is_deprecated
        if self.is_experimental is not None:
            values['is_experimental'] = self.is_experimental
        if self.deprecated is not None:
            values['deprecated'] = self.deprecated
        if self.experimental is not None:
            values['experimental'] = self.experimental
        return values

    def to_xml_doc(self)->Et.Element:
        base_element = self._to_xml()
        base_element.tag = 'method'
        return base_element

class DocMethods(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocMethod, initlist)

    def new(self, **kwargs) -> ClassDocMethod:
        method = ClassDocMethod(**kwargs)
        self.append(method)
        return method

    def to_dict(self) -> dict:
        result = dict()
        result['methods'] = []
        for method in self.data:
            result['methods'].append(method.to_dict())
        return result

    def to_xml_doc(self)->Element:
        element = Et.Element('methods')
        for method in self.data:
          element.append(method.to_xml_doc())
        return element

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocMethod, json_str)

    @classmethod
    def from_xml(cls, element: Element):
        initial_list = [ClassDocMethod.from_xml(e) for e in element]
        return cls(initial_list)