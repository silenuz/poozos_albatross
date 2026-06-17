from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_operators_operator_param import (
    ClassOperatorsOperatorParam,
)
from spirare.caecias.class_doc_operators_operator_return import (
    ClassOperatorsOperatorReturn,
)


@dataclass(slots=True, kw_only=True)
class ClassOperatorsOperator:
    class Meta:
        global_type = False

    return_value: None | ClassOperatorsOperatorReturn = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )
    param: list[ClassOperatorsOperatorParam] = field(
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
