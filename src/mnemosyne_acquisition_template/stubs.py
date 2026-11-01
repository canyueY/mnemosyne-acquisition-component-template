"""All extension points fail explicitly. No networking, storage or policy engine."""

from __future__ import annotations

from typing import Mapping

from .contracts import (
    AcquiredItem,
    AcquisitionBatch,
    AcquisitionRequest,
    CognitionReceipt,
    ConnectionProfile,
    NodeContractReport,
    ResearchDecision,
    ResearchSignals,
    SubmissionReceipt,
)
from .errors import TemplateNotImplementedError
from .ports import MnemosyneBridge, ResearchHook, SourceAdapter


class TemplateSourceAdapter(SourceAdapter):
    def read(self, request: AcquisitionRequest) -> AcquisitionBatch:
        raise TemplateNotImplementedError("Implement source access in a derived component; this template cannot read sources.")

    def normalize(self, raw_record: Mapping[str, object]) -> AcquiredItem:
        raise TemplateNotImplementedError("Implement source-specific normalization in a derived component.")


class TemplateMnemosyneBridge(MnemosyneBridge):
    def inspect_connection(self, profile: ConnectionProfile) -> NodeContractReport:
        raise TemplateNotImplementedError("Implement explicit Node contract discovery in a derived component.")

    def map_observation(self, item: AcquiredItem, profile: ConnectionProfile) -> Mapping[str, object]:
        raise TemplateNotImplementedError("Implement mapping to the installed Node's public Observation contract.")

    def submit_observation(self, payload: Mapping[str, object], profile: ConnectionProfile) -> SubmissionReceipt:
        raise TemplateNotImplementedError("Implement authorized submission in a derived component; this template cannot write memory.")

    def read_cognition_state(self, receipt: SubmissionReceipt, profile: ConnectionProfile) -> CognitionReceipt:
        raise TemplateNotImplementedError("Implement observable receipts without claiming that storage proves cognition.")


class TemplateResearchHook(ResearchHook):
    def assess(self, signals: ResearchSignals, policy: Mapping[str, object]) -> ResearchDecision:
        raise TemplateNotImplementedError("Implement the documented threshold in a derived component; this template cannot evaluate or search.")
