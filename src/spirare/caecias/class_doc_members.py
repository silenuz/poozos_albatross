from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_members_member import ClassMembersMember


@dataclass(slots=True, kw_only=True)
class ClassMembers:
    class Meta:
        global_type = False

    member: list[ClassMembersMember] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
