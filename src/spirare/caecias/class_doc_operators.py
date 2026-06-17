from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_operators_operator import ClassOperatorsOperator


@dataclass(slots=True, kw_only=True)
class ClassOperators:
    class Meta:
        global_type = False

    operator: list[ClassOperatorsOperator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
