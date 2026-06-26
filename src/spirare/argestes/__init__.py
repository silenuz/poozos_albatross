#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: __init__.py

@Author: Phosphor (horuuendillus@gmail.com)
"""
from argestes.doc_base import ClassDocReturn, ClassDocParameter, ClassDocReturnError, DocParameters, \
    DocReturnErrorsList
from .class_doc_operator import ClassDocOperator
from .class_doc_constructor import ClassDocConstructor
from .class_doc_constant import ClassDocConstant
from .class_doc_annotation import ClassDocAnnotation
from .class_doc_member import ClassDocMember
from .class_doc_method import ClassDocMethod
from .class_doc_signal import ClassDocSignal
from .class_doc_theme_item import ClassDocThemeItem

__all__ = [
    'ClassDocReturn',
    'ClassDocParameter',
    'ClassDocConstructor',
    'ClassDocOperator',
    'DocReturnErrorsList',
    'DocParameters',
    'ClassDocReturn',
    'ClassDocConstant',
    'ClassDocAnnotation',
    'ClassDocMember',
    'ClassDocMethod',
    'ClassDocSignal',
    'ClassDocThemeItem',
]
