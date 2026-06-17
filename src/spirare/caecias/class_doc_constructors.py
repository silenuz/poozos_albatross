from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_constructors_constructor import (
    ClassConstructorsConstructor,
)


@dataclass(slots=True, kw_only=True)
class ClassConstructors:
    class Meta:
        global_type = False

    constructor: list[ClassConstructorsConstructor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
