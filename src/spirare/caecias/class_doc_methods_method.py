from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_methods_method_param import ClassMethodsMethodParam
from spirare.caecias.class_doc_methods_method_return import (
    ClassMethodsMethodReturn,
)
from spirare.caecias.class_doc_methods_method_returns_error import (
    ClassMethodsMethodReturnsError,
)


@dataclass(slots=True, kw_only=True)
class ClassMethodsMethod:
    class Meta:
        global_type = False

    return_value: None | ClassMethodsMethodReturn = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )
    returns_error: list[ClassMethodsMethodReturnsError] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    param: list[ClassMethodsMethodParam] = field(
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
