#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocAnnotation.md

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import xml
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et

from .doc_base import MethodReturnBase, ModelCollection, DocParameters,Description, Zucaritas
from .doc_base import ClassDocReturn


class ClassDocAnnotation(MethodReturnBase,Zucaritas):
    """
    This class represents a model of the class docs annotation element
    
    :param str name: The value of the name attribute for the annotation element.
    :param Description description: The value of the description element for the annotation element.
    :param str qualifiers: The value of the qualifiers attribute for the annotation element.
    :param DocParameters parameters: The value of the parameters element for the annotation element.
    :param ClassDocReturn return_value: The value of the return_value element for the annotation element.
    :param str keywords: The value of the keywords attribute for the annotation element.
    """
    __slots__ = ['keywords']
    keywords: str
    """The value of the keywords attribute for the annotation element."""

    def __init__(self, name: str, description: Description=Description(), qualifiers:str=None,
                 parameters: DocParameters = None, return_value: ClassDocReturn = None, keywords:str=None):
        MethodReturnBase.__init__(self, name=name, description=description, qualifiers=qualifiers,parameters=parameters, return_value=return_value)
        self.keywords = keywords
        """The value of the keywords attribute for the annotation element."""

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this annotation element model instance.

       :return: a dictionary of values for this annotation model instance.
       """
        values = super().to_dict()
        if self.keywords is not None:
            values['keywords'] = self.keywords
        return values

    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this annotation model instance.

        :return: A Godot class doc element for this annotation model instance.
        """
        base_element = self._to_xml()
        base_element.tag = 'annotation'
        return base_element

############################################################################################
###                         Annotations List Model                                      ###
###########################################################################################

class DocAnnotations(ModelCollection):
    """
    This class models the annotations element, and contains a list of ClassDocAnnotation instances.

    :param list initlist: A list of ClassDocAnnotation instances.
    """
    def __init__(self,initlist=None):
        super().__init__(ClassDocAnnotation, initlist)

    def new(self, **kwargs) -> ClassDocAnnotation:
        """
        Creates a new ClassDocAnnotation instance and adds it to the list.

        :param kwargs: Keyword arguments for the new ClassDocAnnotation instance.
        :return: The new ClassDocAnnotation instance.
        """
        annotation = ClassDocAnnotation(**kwargs)
        self.append(annotation)
        return annotation

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this annotations' element model instance.

       :return: a dictionary of values for this annotations' model instance.
       """
        result = dict()
        result['annotations'] = []
        for annotation in self.data:
            result['annotations'].append(annotation.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str)->'DocAnnotations':
        """
        Create a new DocAnnotations instance from a JSON string.

        :param json_str: the JSON string containing the annotations' data.
        :return: A new DocAnnotations instance.
        """
        return super().from_json(ClassDocAnnotation, json_str)

    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this annotations list instance.

        :return: A Godot class doc element for this annotations list instance.
        """
        element = Et.Element('annotations')
        for annotation in self.data:
          element.append(annotation.to_xml_doc())
        return element

    @classmethod
    def from_xml(cls, element:xml.etree.ElementTree.Element):
        initial_list = [ClassDocAnnotation.from_xml(e) for e in element]
        return cls(initial_list)

