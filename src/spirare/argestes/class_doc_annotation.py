#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocAnnotation

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from xml.etree.ElementTree import Element

from .doc_base import MethodReturnBase, ModelCollection, DocParameters, JsonBase, GodotBase
from .doc_base import ClassDocReturn


class ClassDocAnnotation(MethodReturnBase,JsonBase,GodotBase):
    __slots__ = ['keywords']
    keywords: str

    def __init__(self, name: str, description: str = None,qualifiers:str=None,
                 parameters: DocParameters = None,return_value: ClassDocReturn = None, keywords:str=None):
        MethodReturnBase.__init__(self, name=name, description=description, qualifiers=qualifiers,parameters=parameters, return_value=return_value)
        self.keywords = keywords

    def to_dict(self) -> dict:
        values = super().to_dict()
        if self.keywords is not None:
            values['keywords'] = self.keywords
        return values

class DocAnnotations(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocAnnotation, initlist)

    def new(self, **kwargs) -> ClassDocAnnotation:
        annotation = ClassDocAnnotation(**kwargs)
        self.append(annotation)
        return annotation

    def to_dict(self) -> dict:
        result = dict()
        result['annotations'] = []
        for annotation in self.data:
            result['annotations'].append(annotation.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocAnnotation, json_str)

    @classmethod
    def from_xml(cls, element:Element):
        initial_list = [ClassDocAnnotation.from_xml(e) for e in element]
        return cls(initial_list)

