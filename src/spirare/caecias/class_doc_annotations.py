from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_annotations_annotation import (
    ClassAnnotationsAnnotation,
)


@dataclass(slots=True, kw_only=True)
class ClassAnnotations:
    class Meta:
        global_type = False

    annotation: list[ClassAnnotationsAnnotation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
