#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/19/26
@File: doc_class_base

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class MemberQualifierBase:
    enum: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_bitfield: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

@dataclass(kw_only=True)
class MethodBase:
    param: list[ClassDocParameter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    description: str = field(
        metadata={
            "type": "Element",
        }
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

@dataclass(kw_only=True)
class MethodReturnBase(MethodBase):
    qualifiers: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    return_value: None | ClassDocReturn = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )

@dataclass(kw_only=True)
class MethodReturnKeyword(MethodReturnBase):
    keywords: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

@dataclass(kw_only=True)
class MethodTagBase:

    is_deprecated: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_experimental: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    deprecated: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    experimental: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

@dataclass(kw_only=True)
class MemberBase(MethodTagBase):
    value: str = field(default="")
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    keywords: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )