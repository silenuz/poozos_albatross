from __future__ import annotations

from dataclasses import dataclass, field

from .class_doc_param import ClassDocParam


@dataclass(slots=True, kw_only=True)
class ClassDocSignal:
    class Meta:
        global_type = False

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

    def __post_init__(self):
        if self.description is None:
            self.description = ""
