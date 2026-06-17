from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_constructors_constructor_param import (
    ClassConstructorsConstructorParam,
)
from spirare.caecias.class_doc_constructors_constructor_return import (
    ClassConstructorsConstructorReturn,
)


@dataclass(slots=True, kw_only=True)
class ClassConstructorsConstructor:
    class Meta:
        global_type = False

    return_value: None | ClassConstructorsConstructorReturn = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )
    param: list[ClassConstructorsConstructorParam] = field(
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
