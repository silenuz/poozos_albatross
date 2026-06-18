from __future__ import annotations

from dataclasses import dataclass, field

from .class_doc_annotation import ClassDocAnnotation
from .class_doc_constant import ClassDocConstant
from .class_doc_constructor import ClassDocConstructor
from .class_doc_member import ClassDocMember
from .class_doc_method import ClassDocMethod
from .class_doc_operator import ClassDocOperator
from .class_doc_signal import ClassDocSignal
from .class_doc_theme_item import ClassDocThemeItem
from .class_doc_tutorials_link import ClassTutorialsLink


@dataclass(slots=True, kw_only=True)
class ClassDocModel:
    class Meta:
        name = "class"

    brief_description: str = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    description: str = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    tutorials: list[ClassTutorialsLink] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )

    constructors: list[ClassDocConstructor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    methods: list[ClassDocMethod] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    members: list[ClassDocMember] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    signals: list[ClassDocSignal] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    constants: list[ClassDocConstant] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    annotations: list[ClassDocAnnotation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    theme_items: list[ClassDocThemeItem] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    operators: list[ClassDocOperator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    inherits: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    api_type: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: None | float = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
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
    keywords: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    def __post_init__(self):
        if self.description is None:
            self.description = ""
        if self.brief_description is None:
            self.brief_description = ""
        if self.tutorials is None:
            self.tutorials = []
