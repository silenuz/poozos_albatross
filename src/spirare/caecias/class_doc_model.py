from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_annotations import ClassAnnotations
from spirare.caecias.class_doc_constants import ClassConstants
from spirare.caecias.class_doc_constructors import ClassConstructors
from spirare.caecias.class_doc_members import ClassMembers
from spirare.caecias.class_doc_methods import ClassMethods
from spirare.caecias.class_doc_operators import ClassOperators
from spirare.caecias.class_doc_signals import ClassSignals
from spirare.caecias.class_doc_theme_items import ClassThemeItems
from spirare.caecias.class_doc_tutorials import ClassTutorials


@dataclass(slots=True, kw_only=True)
class ExtensionDocModel:
    class Meta:
        name = "class"

    brief_description: str = field(
        metadata={
            "type": "Element",
        }
    )
    description: str = field(
        metadata={
            "type": "Element",
        }
    )
    tutorials: ClassTutorials = field(
        metadata={
            "type": "Element",
        }
    )
    constructors: None | ClassConstructors = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    methods: None | ClassMethods = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    members: None | ClassMembers = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    signals: None | ClassSignals = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    constants: None | ClassConstants = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    annotations: None | ClassAnnotations = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    theme_items: None | ClassThemeItems = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    operators: None | ClassOperators = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    inherits: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    api_type: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: None | float = field(
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
