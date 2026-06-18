#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/17/26
@File: extension_doc

@Author: Phosphor (horuuendillus@gmail.com)
"""
from dataclasses import dataclass, field
from .class_doc_model import ClassDocModel


@dataclass(slots=True, kw_only=True)
class ExtensionDocModel:
    class Meta:
        global_type = False

    class_doc: list[ClassDocModel] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )