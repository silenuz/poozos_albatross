from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_annotations_annotation_param import (
    ClassAnnotationsAnnotationParam,
)
from spirare.caecias.class_doc_annotations_annotation_return import (
    ClassAnnotationsAnnotationReturn,
)


@dataclass(slots=True, kw_only=True)
class ClassAnnotationsAnnotation:
    class Meta:
        global_type = False

    return_value: None | ClassAnnotationsAnnotationReturn = field(
        default=None,
        metadata={
            "name": "return",
            "type": "Element",
        },
    )
    param: list[ClassAnnotationsAnnotationParam] = field(
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
    keywords: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
