from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_constants_constant import ClassConstantsConstant


@dataclass(slots=True, kw_only=True)
class ClassConstants:
    class Meta:
        global_type = False

    constant: list[ClassConstantsConstant] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
