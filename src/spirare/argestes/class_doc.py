#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/19/26
@File: doc_class

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import json
import xml
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et
from pathlib import Path

from .class_doc_annotation import DocAnnotations
from .class_doc_constant import DocConstants
from .class_doc_constructor import DocConstructors
from .class_doc_member import DocMembers
from .class_doc_method import DocMethods
from .class_doc_operator import DocOperators
from .class_doc_signal import DocSignals
from .class_doc_theme_item import DocThemeItems
from .doc_base import DocTutorials, BriefDescription, Description, Zucaritas


class ClassDocModel(Zucaritas):
    """
    This class represents a model of the root class element of the Godot doc xml.

    :param str name: The value of the name attribute for this class element.
    :param BriefDescription brief_description: The value of the brief_description element for this class element.
    :param Description description: The value of the description element for this class element.
    :param DocAnnotations annotations: The value of the annotations element for this class element.
    :param DocConstants constants: The value of the constants element for this class element.
    :param DocConstructors constructors: The value of the constructors element for this class element.
    :param DocMembers members: The value of the members element for this class element.
    :param DocMethods methods: The value of the methods element for this class element.
    :param DocOperators operators: The value of the operators element for this class element.
    :param DocSignals signals: The value of the signals element for this class element.
    :param DocThemeItems theme_items: The value of the theme_items element for this class element.
    :param DocTutorials tutorials: The value of the tutorials element for this class element.
    :param str inherits: The value of the inherits attribute for this class element.
    :param str api_type: The value of the api_type attribute for this class element.
    :param float version: The value of the version attribute for this class element.
    :param bool is_deprecated: The value of the is_deprecated attribute for this class element.
    :param bool is_experimental: The value of the is_experimental attribute for this class element.
    :param str deprecated: The value of the deprecated attribute for this class element.
    :param str experimental: The value of the experimental attribute for this class element.
    :param str keywords: The value of the keywords attribute for this class element.

    "Your going to need a bigger boat"
    """
    __slots__ = ('name', 'brief_description', 'description', 'tutorials', 'annotations', 'constructors','methods',
                 'members','signals','constants','operators','theme_items','inherits','api_type','version',
                 'is_deprecated','is_experimental','deprecated','experimental','keywords')
    name: str
    """The value of the name attribute for this class element."""
    brief_description: BriefDescription
    """The value of the brief_description element for this class element."""
    description: Description
    """The value of the description element for this class element."""
    annotations: DocAnnotations
    """The value of the annotations element for this class element."""
    constants: DocConstants
    """The value of the constants element for this class element."""
    constructors:DocConstructors
    """The value of the constructors element for this class element."""
    members:DocMembers
    """The value of the members element for this class element."""
    methods: DocMethods
    """The value of the methods element for this class element."""
    operators: DocOperators
    """The value of the operators element for this class element."""
    signals: DocSignals
    """The value of the signals element for this class element."""
    theme_items: DocThemeItems
    """The value of the theme_items element for this class element."""
    tutorials: DocTutorials
    """The value of the tutorials element for this class element."""
    inherits:str
    """The value of the inherits attribute for this class element."""
    api_type:str
    """The value of the api_type attribute for this class element."""
    version:float
    """The value of the version attribute for this class element."""
    is_deprecated:bool
    """The value of the is_deprecated attribute for this class element."""
    is_experimental:bool
    """The value of the is_experimental attribute for this class element."""
    deprecated:str
    """The value of the deprecated attribute for this class element."""
    experimental:str
    """The value of the experimental attribute for this class element."""
    keywords:str
    """The value of the keywords attribute for this class element."""

    def __init__(self, name: str, brief_description: BriefDescription = BriefDescription(), description: Description = Description(), annotations: DocAnnotations = None,
                 constructors: DocConstructors = None, constants:DocConstants=None, members:DocMembers=None, methods: DocMethods = None, operators: DocOperators=None,
                 signals: DocSignals=None, theme_items: DocThemeItems=None, keywords: str = None, tutorials:DocTutorials = DocTutorials(),
                 inherits: str = None, api_type: str=None, version: float = None, is_deprecated: bool = None, is_experimental: bool = None,
                 deprecated: str = None, experimental: str = None) -> None:
        self.name = name
        """The value of the name attribute for this class element."""
        self.brief_description = brief_description
        """The value of the brief_description element for this class element."""
        self.description = description
        """The value of the description element for this class element."""
        self.annotations = annotations
        """The value of the annotations element for this class element."""
        self.constructors = constructors
        """The value of the constructors element for this class element."""
        self.constants = constants
        """The value of the constants element for this class element."""
        self.members = members
        """The value of the members element for this class element."""
        self.methods = methods
        """The value of the methods element for this class element."""
        self.operators = operators
        """The value of the operators element for this class element."""
        self.signals = signals
        """The value of the operators element for this class element."""
        self.theme_items = theme_items
        """The value of the theme_items element for this class element."""
        self.keywords = keywords
        """The value of the keywords attribute for this class element."""
        self.tutorials = tutorials
        """The value of the tutorials element for this class element."""
        self.inherits = inherits
        """The value of the inherits attribute for this class element."""
        self.api_type = api_type
        """The value of the api_type attribute for this class element."""
        self.version = version
        """The value of the version attribute for this class element."""
        self.is_deprecated = is_deprecated
        """The value of the is_deprecated attribute for this class element."""
        self.is_experimental = is_experimental
        """The value of the is_experimental attribute for this class element."""
        self.deprecated = deprecated
        """The value of the deprecated attribute for this class element."""
        self.experimental = experimental
        """The value of the experimental attribute for this class element."""
        self.__post_init__()

    def __post_init__(self):
        if isinstance(self.description, str):
            self.description = Description(text=self.description)
        if isinstance(self.brief_description, str):
            self.brief_description = BriefDescription(text=self.brief_description)

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this class doc root element model instance.

       :return: a dictionary of values for this class doc root model instance.
       """
        result = dict()
        result['name'] = self.name
        result.update(self.brief_description.to_dict())
        result.update(self.description.to_dict())
        result.update(self.tutorials.to_dict())
        if self.constructors is not None:
            result.update(self.constructors.to_dict())
        if self.methods is not None:
            result.update(self.methods.to_dict())
        if self.members is not None:
            result.update(self.members.to_dict())
        if self.signals is not None:
            result.update(self.signals.to_dict())
        if self.constants is not None:
            result.update(self.constants.to_dict())
        if self.operators is not None:
            result.update(self.operators.to_dict())
        if self.theme_items is not None:
            result.update(self.theme_items.to_dict())
        if self.annotations is not None:
            result.update(self.annotations.to_dict())
        if self.keywords is not None:
            result['keywords'] = self.keywords
        if self.inherits is not None:
            result['inherits'] = self.inherits
        if self.api_type is not None:
            result['api_type'] = self.api_type
        if self.version is not None:
            result['version'] = self.version
        if self.is_deprecated is not None:
            result['is_deprecated'] = self.is_deprecated
        if self.is_experimental is not None:
            result['is_experimental'] = self.is_experimental
        if self.deprecated is not None:
            result['deprecated'] = self.deprecated
        if self.experimental is not None:
            result['experimental'] = self.experimental
        return result

    def to_xml_doc(self) -> xml.etree.ElementTree.Element:
        """
        Create a Godot class doc root element for this model instance.

        :return: A Godot class doc root element for this model instance.
        """
        base_element = self._to_xml()
        base_element.tag = 'class'
        return base_element


    @classmethod
    def from_file(cls, file_path: Path) -> 'ClassDocModel':
        if isinstance(file_path, str):
            file_path = Path(file_path)
        ext = file_path.suffix
        if ext == '.xml':
            tree = Et.parse(str(file_path))
            root = tree.getroot()
            return cls.from_xml(root)
        elif ext == '.json':
            with open(file_path, "r", encoding="utf-8") as file:
                data = file_path.read_text()
                return cls.from_json(data)
        else:
            raise TypeError(f'Unsupported file extension: {ext}')

class ExtensionDocModel:
    class_doc: list[ClassDocModel]