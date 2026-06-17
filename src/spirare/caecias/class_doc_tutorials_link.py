from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class ClassTutorialsLink:
    class Meta:
        global_type = False

    value: str = field(default="")
    title: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
