#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/19/26
@File: doc_class_elements

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from __future__ import annotations

from builtins import list
from dataclasses import dataclass, field
from .class_doc_base import *

@dataclass(slots=True, kw_only=True)
class ClassDocAnnotation(MethodReturnKeyword):
    """
    This class represents a model of the Annotation element of the GDExtension class documentation XML
    :param list[ClassDocParameter] param: The value of the param attribute for this element.
    :param str description: The value of the description attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str qualifiers: The value of the qualifiers attribute for this element.  (default: None )
    :param  DocReturnBase return_value: The value of the return_value attribute for this element.  (default: None )
    :param  str keywords: The value of the keywords attribute for this element.  (default: None )
    """
    pass

@dataclass(slots=True, kw_only=True)
class ClassDocConstant(MemberBase, DocQualifierBase):
    """
    This class represents a model of the Constant element of the GDExtension class documentation XML
    :param  str enum: The value of the enum attribute for this element.  (default: None )
    :param  bool is_bitfield: The value of the is_bitfield attribute for this element.  (default: None )
    :param  bool is_deprecated: The value of the is_deprecated attribute for this element.  (default: None )
    :param  bool is_experimental: The value of the is_experimental attribute for this element.  (default: None )
    :param  str deprecated: The value of the deprecated attribute for this element.  (default: None )
    :param  str experimental: The value of the experimental attribute for this element.  (default: None )
    :param str value: The value of the value attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str keywords: The value of the keywords attribute for this element.  (default: None )
    :param  str value_attribute: The value of the value_attribute attribute for this element.  (default: None )
    """

    value_attribute: None | str = field(
        default=None,
        metadata={
            "name": "value",
            "type": "Attribute",
        },
    )

@dataclass(slots=True, kw_only=True)
class ClassDocConstructor(MethodReturnBase):
    """
    This class represents a model of the Constructor element of the GDExtension class documentation XML
    :param list[ClassDocParameter] param: The value of the param attribute for this element.
    :param str description: The value of the description attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str qualifiers: The value of the qualifiers attribute for this element.  (default: None )
    :param  DocReturnBase return_value: The value of the return_value attribute for this element.  (default: None )
    """
    pass


@dataclass(slots=True, kw_only=True)
class ClassDocMember(ClassDocConstant):
    """
    This class represents a model of the Member element of the GDExtension class documentation XML
    :param  str enum: The value of the enum attribute for this element.  (default: None )
    :param  bool is_bitfield: The value of the is_bitfield attribute for this element.  (default: None )
    :param  bool is_deprecated: The value of the is_deprecated attribute for this element.  (default: None )
    :param  bool is_experimental: The value of the is_experimental attribute for this element.  (default: None )
    :param  str deprecated: The value of the deprecated attribute for this element.  (default: None )
    :param  str experimental: The value of the experimental attribute for this element.  (default: None )
    :param str value: The value of the value attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str keywords: The value of the keywords attribute for this element.  (default: None )
    :param  str value_attribute: The value of the value_attribute attribute for this element.  (default: None )
    :param  str type_value: The value of the type_value attribute for this element.  (default: None )
    :param  str setter: The value of the setter attribute for this element.  (default: None )
    :param  str getter: The value of the getter attribute for this element.  (default: None )
    :param  str overrides: The value of the overrides attribute for this element.  (default: None )
    :param  str default: The value of the default attribute for this element.  (default: None )
    """

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
class ClassDocMethod(MethodReturnKeyword, MethodTagBase):
    """
    This class represents a model of the Method element of the GDExtension class documentation XML
    :param  bool is_deprecated: The value of the is_deprecated attribute for this element.  (default: None )
    :param  bool is_experimental: The value of the is_experimental attribute for this element.  (default: None )
    :param  str deprecated: The value of the deprecated attribute for this element.  (default: None )
    :param  str experimental: The value of the experimental attribute for this element.  (default: None )
    :param list[ClassDocParameter] param: The value of the param attribute for this element.
    :param str description: The value of the description attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str qualifiers: The value of the qualifiers attribute for this element.  (default: None )
    :param  DocReturnBase return_value: The value of the return_value attribute for this element.  (default: None )
    :param  str keywords: The value of the keywords attribute for this element.  (default: None )
    :param list[ClassDocReturnsError] returns_error: The value of the returns_error attribute for this element.
    """

    returns_error: list[ClassDocReturnsError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassDocOperator(MethodReturnBase):
    """
    This class represents a model of the Operator element of the GDExtension class documentation XML
    :param list[ClassDocParameter] param: The value of the param attribute for this element.
    :param str description: The value of the description attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str qualifiers: The value of the qualifiers attribute for this element.  (default: None )
    :param  DocReturnBase return_value: The value of the return_value attribute for this element.  (default: None )
    """
    pass

@dataclass(slots=True, kw_only=True)
class ClassDocParameter(DocParameterBase):
    """
    This class represents a model of the Parameter element of the GDExtension class documentation XML
    :param  str enum: The value of the enum attribute for this element.  (default: None )
    :param  bool is_bitfield: The value of the is_bitfield attribute for this element.  (default: None )
    :param  str type_value: The value of the type_value attribute for this element.  (default: None )
    :param  int index: The value of the index attribute for this element.  (default: None )
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str default: The value of the default attribute for this element.  (default: None )
    """
    pass


@dataclass(slots=True, kw_only=True)
class ClassDocReturn(DocQualifierBase):
    """
    This class represents a model of the Return element of the GDExtension class documentation XML
    :param  str enum: The value of the enum attribute for this element.  (default: None )
    :param  bool is_bitfield: The value of the is_bitfield attribute for this element.  (default: None )
    :param  str type_value: The value of the type_value attribute for this element.  (default: None )
    """

    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassDocReturnsError:
    """
    This class represents a model of the ReturnsError element of the GDExtension class documentation XML
    :param  int number: The value of the number attribute for this element.  (default: None )
    """

    number: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(slots=True, kw_only=True)
class ClassDocSignal(MethodBase, MethodTagBase):
    """
    This class represents a model of the Signal element of the GDExtension class documentation XML
    :param  bool is_deprecated: The value of the is_deprecated attribute for this element.  (default: None )
    :param  bool is_experimental: The value of the is_experimental attribute for this element.  (default: None )
    :param  str deprecated: The value of the deprecated attribute for this element.  (default: None )
    :param  str experimental: The value of the experimental attribute for this element.  (default: None )
    :param list[ClassDocParameter] param: The value of the param attribute for this element.
    :param str description: The value of the description attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    """
    pass


@dataclass(slots=True, kw_only=True)
class ClassDocThemeItem(MemberBase):
    """
    This class represents a model of the ThemeItem element of the GDExtension class documentation XML
    :param  bool is_deprecated: The value of the is_deprecated attribute for this element.  (default: None )
    :param  bool is_experimental: The value of the is_experimental attribute for this element.  (default: None )
    :param  str deprecated: The value of the deprecated attribute for this element.  (default: None )
    :param  str experimental: The value of the experimental attribute for this element.  (default: None )
    :param str value: The value of the value attribute for this element.
    :param  str name: The value of the name attribute for this element.  (default: None )
    :param  str keywords: The value of the keywords attribute for this element.  (default: None )
    :param  str data_type: The value of the data_type attribute for this element.  (default: None )
    :param  str type_value: The value of the type_value attribute for this element.  (default: None )
    :param  str default: The value of the default attribute for this element.  (default: None )
    """
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
    """
    This class represents a model of the Link element of the GDExtension class documentation XML
    :param str value: The value of the value attribute for this element.
    :param  str title: The value of the title attribute for this element.  (default: None )
    """

    value: str = field(default="")
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )