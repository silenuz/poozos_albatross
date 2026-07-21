#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: godot_doc_model
@Date: 6/23/26
@File: ClassDocThemeItem

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import xml
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et

from .doc_base import ModelCollection
from .zucaritas import Zucaritas


class ClassDocThemeItem(Zucaritas):
    """
    This class represents a model of the class doc's theme_item element
    
    :param str name: The value of the name attribute for the theme_item element.
    :param str text: The value of the text attribute for the theme_item element.
    :param str data_type: The value of the data_type attribute for the theme_item element.
    :param str type_value: The value of the type attribute for the theme_item element.
    :param str default: The value of the default attribute for the theme_item element.
    :param str keywords: The value of the keywords attribute for the theme_item element.
    :param str deprecated: The value of the deprecated attribute for the theme_item element.
    :param str experimental: The value of the experimental attribute for the theme_item element.

    "There's no place like home"
    """
    __slots__ = ("name", "text", "data_type", "type_value", "default", "keywords", "deprecated", "experimental")
    name: str
    """The value of the name attribute for the theme_item element."""
    text: str
    """The text value for this element."""
    data_type: str
    """The value of the data_type attribute for the theme_item element"""
    type_value: str
    """The value of the type attribute for the theme_item element."""
    default: str
    """The value of the default attribute for the theme_item element."""
    keywords: str
    """The value of the keywords attribute for the theme_item element"""
    deprecated: str
    """The value of the deprecated attribute for the theme_item element"""
    experimental: str
    """The value of the experimental attribute for the theme_item element"""

    def __init__(self, name: str, text: str = None, data_type: str = None, type_value: str = None,
                 default: str = None, keywords: str = None, deprecated: str = None, experimental: str = None):
        self.name = name
        """The value of the name attribute for the theme_item element."""
        self.text = text
        """The text value for this element."""
        self.data_type = data_type
        """The value of the data_type attribute for the theme_item element"""
        self.type_value = type_value
        """The value of the type attribute for the theme_item element."""
        self.default = default
        """The value of the default attribute for the theme_item element."""
        self.keywords = keywords
        """The value of the keywords attribute for the theme_item element"""
        self.deprecated = deprecated
        """The value of the deprecated attribute for the theme_item element"""
        self.experimental = experimental
        """The value of the experimental attribute for the theme_item element"""

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this theme_item element model instance.

       :return: a dictionary of values for this theme_item model instance.
       """
        values = dict()
        if self.name is not None:
            values['name'] = self.name
        if self.text is not None:
            values['text'] = self.text
        if self.data_type is not None:
            values['data_type'] = self.data_type
        if self.type_value is not None:
            values['type_value'] = self.type_value
        if self.default is not None:
            values['default'] = self.default
        if self.keywords is not None:
            values['keywords'] = self.keywords
        if self.deprecated is not None:
            values['deprecated'] = self.deprecated
        if self.experimental is not None:
            values['experimental'] = self.experimental
        return values

    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this theme_item model instance.

        :return: A Godot class doc element for this theme_item model instance.
        """
        base_element = self._to_xml()
        base_element.tag = 'theme_item'
        return base_element



############################################################################################
###                         ThemeItems List Model                                      ###
###########################################################################################


class DocThemeItems(ModelCollection):
    """
    This class models the theme_items element, and contains a list of ClassDocThemeItem instances.

    :param list initlist: A list of ClassDocThemeItem instances.

    “Did I ever tell you the definition of insanity?”
    """
    def __init__(self, initlist=None):
        super().__init__(ClassDocThemeItem, initlist)

    def new(self, **kwargs) -> ClassDocThemeItem:
        """
        Creates a new ClassDocThemeItem instance and adds it to the list.

        :param kwargs: Keyword arguments for the new ClassDocThemeItem instance.
        :return: The new ClassDocThemeItem instance.
        """
        theme_item = ClassDocThemeItem(**kwargs)
        self.append(theme_item)
        return theme_item

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this theme_items' element model instance.

       :return: a dictionary of values for this theme_items' model instance.
       """
        result = dict()
        result['theme_items'] = []
        for theme_item in self.data:
            result['theme_items'].append(theme_item.to_dict())
        return result


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this theme_items list instance.

        :return: A Godot class doc element for this theme_items list instance.
        """
        element = Et.Element('theme_items')
        for theme_item in self.data:
          element.append(theme_item.to_xml_doc())
        return element


    @classmethod
    def from_json(cls, json_str: str)->'DocThemeItems':
        """
        Create a new DocThemeItems instance from a JSON string.

        :param json_str: the JSON string containing the theme_items' data.
        :return: A new DocThemeItems instance.
        """
        return super().from_json(ClassDocThemeItem, json_str)

    @classmethod
    def from_xml(cls, element: xml.etree.ElementTree.Element):
        initial_list = [ClassDocThemeItem.from_xml(e) for e in element]
        return cls(initial_list)
