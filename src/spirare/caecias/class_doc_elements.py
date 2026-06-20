#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/19/26
@File: doc_class_elements

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from .class_doc_base import *

@dataclass(slots=True, kw_only=True)
class ClassDocAnnotation(MethodReturnKeyword):
    pass

@dataclass(slots=True, kw_only=True)
class ClassDocConstant(MemberBase, MemberQualifierBase):

    value_attribute: None | str = field(
        default=None,
        metadata={
            "name": "value",
            "type": "Attribute",
        },
    )

@dataclass(slots=True, kw_only=True)
class ClassDocConstructor(MethodReturnBase):
    pass


@dataclass(slots=True, kw_only=True)
class ClassDocMember(ClassDocConstant):

    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    setter: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    getter: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    overrides: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    default: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassDocMethod(MethodReturnKeyword,MethodTagBase):

    returns_error: list[ClassDocReturnsError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassDocOperator(MethodReturnBase):
    pass

@dataclass(slots=True, kw_only=True)
class ClassDocParameter(MethodParameterBase):
    pass


@dataclass(slots=True, kw_only=True)
class ClassDocReturn(MemberQualifierBase):

    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassDocReturnsError:

    number: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassDocSignal(MethodBase,MethodTagBase):
    pass


@dataclass(slots=True, kw_only=True)
class ClassDocThemeItem(MemberBase):
    data_type: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    default: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassTutorialsLink:

    value: str = field(default="")
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )