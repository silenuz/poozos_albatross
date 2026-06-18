from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ClassDocReturnsError:
    class Meta:
        global_type = False

    number: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
