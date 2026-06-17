from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_tutorials_link import ClassTutorialsLink


@dataclass(slots=True, kw_only=True)
class ClassTutorials:
    class Meta:
        global_type = False

    link: list[ClassTutorialsLink] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
