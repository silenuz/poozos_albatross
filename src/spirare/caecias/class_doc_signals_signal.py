from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_signals_signal_param import ClassSignalsSignalParam


@dataclass(slots=True, kw_only=True)
class ClassSignalsSignal:
    class Meta:
        global_type = False

    param: list[ClassSignalsSignalParam] = field(
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
