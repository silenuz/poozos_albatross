#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocSignal

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import xml
from xml.etree import ElementTree as Et
from xml.etree.ElementTree import Element

from .doc_base import MethodBase,ModelCollection, DocParameters, DocDescription, Zucaritas


class ClassDocSignal(MethodBase,Zucaritas):
    """
    This class represents a model of the class doc's signal element
    
    :param str name: The value of the name attribute for the signal element.
    :param DocDescription description: The value of the description element for the signal element.
    :param str qualifiers: The value of the qualifiers attribute for the signal element.
    :param DocParameters parameters: The value of the parameters element for the signal element.
    :param bool is_deprecated: The value of the is_deprecated attribute for the signal element.
    :param str deprecated: The value of the deprecated attribute for the signal element.
    :param bool is_experimental: The value of the is_experimental attribute for the signal element.
    :param str experimental: The value of the experimental attribute for the signal element.

    "Well here's another nice mess you've gotten me into"
    """
    __slots__ = ('is_deprecated', 'deprecated','is_experimental','experimental')
    is_deprecated: bool
    deprecated: str
    is_experimental: bool
    experimental: str

    def __init__(self,name:str,description:DocDescription=DocDescription(), parameters:DocParameters=None,
                 qualifiers: str = None, is_deprecated: bool=None, deprecated: str = None, is_experimental: bool=None,
                 experimental: str=None) -> None:
        super().__init__(name=name,description=description,parameters=parameters,qualifiers=qualifiers)
        self.is_deprecated = is_deprecated
        self.deprecated = deprecated
        self.is_experimental = is_experimental
        self.experimental = experimental

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this signal element model instance.

       :return: a dictionary of values for this signal model instance.
       """
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

    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        base_element = self._to_xml()
        base_element.tag = 'signal'
        return base_element


############################################################################################
###                         Signals List Model                                          ###
###########################################################################################


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


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        element = Et.Element('signals')
        for signal in self.data:
          element.append(signal.to_xml_doc())
        return element


    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocSignal, json_str)

    @classmethod
    def from_xml(cls, element:xml.etree.ElementTree.Element):
        initial_list = [ClassDocSignal.from_xml(e) for e in element]
        return cls(initial_list)