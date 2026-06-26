#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/19/26
@File: doc_class

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""

from .class_doc_annotation import DocAnnotations
from .class_doc_constant import DocConstants
from .class_doc_constructor import DocConstructors
from .class_doc_member import DocMembers
from .class_doc_method import DocMethods
from .class_doc_operator import DocOperators
from .class_doc_signal import DocSignals
from .class_doc_theme_item import DocThemeItems
from .doc_base import JsonBase, GodotBase, DocTutorials, DocBriefDescription, DocDescription


class ClassDocModel(JsonBase,GodotBase):
    __slots__ = ('name', 'brief_description', 'description', 'tutorials', 'annotations', 'constructors','methods',
                 'members','signals','constants','operators','theme_items','inherits','api_type','version',
                 'is_deprecated','is_experimental','deprecated','experimental','keywords')
    name: str
    brief_description: DocBriefDescription
    description: DocDescription
    annotations: DocAnnotations
    constants: DocConstants
    constructors:DocConstructors
    members:DocMembers
    methods: DocMethods
    operators: DocOperators
    signals: DocSignals
    theme_items: DocThemeItems
    ######
    # placeholders
    ##########################
    tutorials: DocTutorials
    ##########################
    inherits:str
    api_type:str
    version:float
    is_deprecated:bool
    is_experimental:bool
    deprecated:str
    experimental:str
    keywords:str

    def __init__(self, name: str, brief_description: DocBriefDescription = DocBriefDescription, description: DocDescription = DocDescription, annotations: DocAnnotations = None,
                 constructors: DocConstructors = None, constants:DocConstants=None,members:DocMembers=None , methods: DocMethods = None, operators: DocOperators=None,
                 signals: DocSignals=None, theme_items: DocThemeItems=None, keywords: str = None, tutorials: str = None,
                 inherits: str = None, api_type: str=None, version: float = None, is_deprecated: bool = None, is_experimental: bool = None,
                 deprecated: str = None, experimental: str = None) -> None:
        self.name = name
        self.brief_description = brief_description
        self.description = description
        self.annotations = annotations
        self.constructors = constructors
        self.constants = constants
        self.members = members
        self.methods = methods
        self.operators = operators
        self.signals = signals
        self.theme_items = theme_items
        self.keywords = keywords
        self.tutorials = tutorials
        self.inherits = inherits
        self.api_type = api_type
        self.version = version
        self.is_deprecated = is_deprecated
        self.is_experimental = is_experimental
        self.deprecated = deprecated
        self.experimental = experimental

    def to_dict(self) -> dict:
        result = dict()
        result['name'] = self.name
        result.update(self.brief_description.to_dict())
        result.update(self.description.to_dict())
        if self.annotations is not None:
            result.update(self.annotations.to_dict())
        if self.constructors is not None:
            result.update(self.constructors.to_dict())
        if self.constants is not None:
            result.update(self.constants.to_dict())
        if self.members is not None:
            result.update(self.members.to_dict())
        if self.methods is not None:
            result.update(self.methods.to_dict())
        if self.operators is not None:
            result.update(self.operators.to_dict())
        if self.signals is not None:
            result.update(self.signals.to_dict())
        if self.theme_items is not None:
            result.update( self.theme_items.to_dict())
        if self.keywords is not None:
            result['keywords'] = self.keywords
        if self.tutorials is not None:
            result.update(self.tutorials.to_dict())
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

class ExtensionDocModel:
    class_doc: list[ClassDocModel]