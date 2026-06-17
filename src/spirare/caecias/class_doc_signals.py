from __future__ import annotations

from dataclasses import dataclass, field

from spirare.caecias.class_doc_signals_signal import ClassSignalsSignal


@dataclass(slots=True, kw_only=True)
class ClassSignals:
    class Meta:
        global_type = False

    signal: list[ClassSignalsSignal] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
