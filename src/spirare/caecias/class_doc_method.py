from __future__ import annotations

from dataclasses import dataclass, field

from .class_doc_return import ClassDocReturn
from .class_doc_param import ClassDocParam
from .class_doc_returns_error import ClassDocReturnsError

@dataclass(slots=True, kw_only=True)
class ClassDocMethod:
    class Meta:
        global_type = False

    return_value: None | ClassDocReturn = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )
    returns_error: list[ClassDocReturnsError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    param: list[ClassDocParam] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    description: str = field(
        default=None,
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
    qualifiers: None | str = field(
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

