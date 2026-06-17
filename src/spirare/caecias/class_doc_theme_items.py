from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_theme_items_theme_item import (
    ClassThemeItemsThemeItem,
)


@dataclass(slots=True, kw_only=True)
class ClassThemeItems:
    class Meta:
        global_type = False

    theme_item: list[ClassThemeItemsThemeItem] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
