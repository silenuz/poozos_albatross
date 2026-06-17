from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ClassConstantsConstant:
    class Meta:
        global_type = False

    value: str = field(default="")
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    value_attribute: None | str = field(
        default=None,
        metadata={
            "name": "value",
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
