from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ClassOperatorsOperatorParam:
    class Meta:
        global_type = False

    index: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    enum: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_bitfield: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    default: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
