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
    Description, Zucaritas


class ClassDocOperator(MethodReturnBase,Zucaritas):
    """
    This class represents a model of the class doc's operator element
    
    :param str name: The value of the name attribute for the operator element.
    :param Description description: The value of the description element for the operator element.
    :param str qualifiers: The value of the qualifiers attribute for the operator element.
    :param DocParameters parameters: The value of the parameters element for the operator element.
    :param ClassDocReturn return_value: The value of the return_value element for the operator element.

    "What we've got here is failure to communicate"
    """
    __slots__ = ()

    def __init__(self, name:str, description:Description=Description(), qualifiers:str=None,
                 return_value: ClassDocReturn = None, parameters: DocParameters = None):
        MethodReturnBase.__init__(self, name=name, description=description,qualifiers=qualifiers,
                                  parameters=parameters,return_value=return_value)


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this operator model instance.

        :return: A Godot class doc element for this operator model instance.
        """
        base_element = self._to_xml()
        base_element.tag = 'operator'
        return base_element


############################################################################################
###                         Operators List Model                                         ###
###########################################################################################


class DocOperators(ModelCollection):
    """
    This class models the operators element, and contains a list of ClassDocOperator instances.

    :param list initlist: A list of ClassDocOperator instances.
    """
    def __init__(self,initlist=None):
        super().__init__(ClassDocOperator, initlist)

    def new(self, **kwargs) -> ClassDocOperator:
        """
        Creates a new ClassDocOperator instance and adds it to the list.

        :param kwargs: Keyword arguments for the new ClassDocOperator instance.
        :return: The new ClassDocOperator instance.
        """
        operator = ClassDocOperator(**kwargs)
        self.append(operator)
        return operator

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this operators' element model instance.

       :return: a dictionary of values for this operators' model instance.
       """
        result = dict()
        result['operators'] = []
        for method in self.data:
            result['operators'].append(method.to_dict())
        return result


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this operators list instance.

        :return: A Godot class doc element for this operators list instance.
        """
        element = Et.Element('operators')
        for operator in self.data:
          element.append(operator.to_xml_doc())
        return element

    @classmethod
    def from_json(cls, json_str: str)->'DocOperators':
        """
        Create a new DocOperators instance from a JSON string.

        :param json_str: the JSON string containing the operators' data.
        :return: A new DocOperators instance.
        """
        return super().from_json(ClassDocOperator, json_str)

    @classmethod
    def from_xml(cls, element: xml.etree.ElementTree.Element):
        initial_list = [ClassDocOperator.from_xml(e) for e in element]
        return cls(initial_list)