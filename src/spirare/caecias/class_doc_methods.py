from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_methods_method import ClassMethodsMethod


@dataclass(slots=True, kw_only=True)
class ClassMethods:
    class Meta:
        global_type = False

    method: list[ClassMethodsMethod] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
