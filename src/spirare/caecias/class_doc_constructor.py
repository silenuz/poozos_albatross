from __future__ import annotations

from dataclasses import dataclass, field


from .class_doc_return import ClassDocReturn
from .class_doc_param import ClassDocParam


@dataclass(slots=True, kw_only=True)
class ClassDocConstructor:
    class Meta:
        global_type = False

    return_value: None | ClassDocReturn = field(
        default=None,
        metadata={
            "name": "return",
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
