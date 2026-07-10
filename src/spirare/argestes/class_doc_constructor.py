#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocConstructor

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import xml
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et

from . import ClassDocReturn
from .doc_base import MethodReturnBase, ModelCollection, DocParameters, Description, Zucaritas


class ClassDocConstructor(MethodReturnBase,Zucaritas):
    """
    This class represents a model of the class docs constructor element
    
    :param str name: The value of the name attribute for the constructor element.
    :param Description description: The value of the description element for the constructor element.
    :param str qualifiers: The value of the qualifiers attribute for the constructor element.
    :param DocParameters parameters: The value of the parameters element for the constructor element.
    :param ClassDocReturn return_value: The value of the return_value element for the constructor element.

    "Soylent Green is people!"
    """
    __slots__ = ()

    def __init__(self, name:str, description:Description=Description(), qualifiers:str=None,
                 parameters: DocParameters = None, return_value: ClassDocReturn = None):
        MethodReturnBase.__init__(self, name=name, description=description,qualifiers=qualifiers,
                                  parameters=parameters, return_value=return_value)


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this constructor model instance.

        :return: A Godot class doc element for this constructor model instance.
        """
        base_element = self._to_xml()
        base_element.tag = 'constructor'
        return base_element


############################################################################################
###                         Constructors List Model                                      ###
###########################################################################################


class DocConstructors(ModelCollection):
    """
    This class models the constructors element, and contains a list of ClassDocConstructor instances.

    :param list initlist: A list of ClassDocConstructor instances.
    """
    def __init__(self,initlist=None):
        super().__init__(ClassDocConstructor, initlist)

    def new(self, **kwargs) -> ClassDocConstructor:
        """
        Creates a new ClassDocConstructor instance and adds it to the list.

        :param kwargs: Keyword arguments for the new ClassDocConstructor instance.
        :return: The new ClassDocConstructor instance.
        """
        constructor = ClassDocConstructor(**kwargs)
        self.append(constructor)
        return constructor

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this constructors' element model instance.

       :return: a dictionary of values for this constructors' model instance.
       """
        result = dict()
        result['constructors'] = []
        for constructor in self.data:
            result['constructors'].append(constructor.to_dict())
        return result

    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this constructors list instance.

        :return: A Godot class doc element for this constructors' list instance.
        """
        element = Et.Element('constructors')
        for constructor in self.data:
          element.append(constructor.to_xml_doc())
        return element


    @classmethod
    def from_json(cls, json_str: str)->'DocConstructors':
        """
        Create a new DocConstructors instance from a JSON string.

        :param json_str: the JSON string containing the constructors' data.
        :return: A new DocConstructors instance.
        """
        return super().from_json(ClassDocConstructor, json_str)

    @classmethod
    def from_xml(cls, element:xml.etree.ElementTree.Element):
        initial_list = [ClassDocConstructor.from_xml(e) for e in element]
        return cls(initial_list)