from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ClassDocMember:
    class Meta:
        global_type = False

    value: str = field(default="")
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
    setter: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    getter: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    overrides: None | str = field(
        default=None,
        metadata={
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
