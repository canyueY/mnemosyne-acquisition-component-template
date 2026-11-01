"""Abstract extension points; no implementations or implicit fallbacks."""

from __future__ import annotations

from abc import ABC, abstractmethod
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


class SourceAdapter(ABC):
    @abstractmethod
    def read(self, request: AcquisitionRequest) -> AcquisitionBatch:
        """Implement permission-aware source access in a derived component."""
        raise NotImplementedError

    @abstractmethod
    def normalize(self, raw_record: Mapping[str, object]) -> AcquiredItem:
        """Preserve provenance and scope; do not promote source claims to truth."""
        raise NotImplementedError


class MnemosyneBridge(ABC):
    @abstractmethod
    def inspect_connection(self, profile: ConnectionProfile) -> NodeContractReport:
        """Implement public contract discovery; never inspect core SQLite."""
        raise NotImplementedError

    @abstractmethod
    def map_observation(self, item: AcquiredItem, profile: ConnectionProfile) -> Mapping[str, object]:
        """Map only after confirming the installed Node's schema and grants."""
        raise NotImplementedError

    @abstractmethod
    def submit_observation(self, payload: Mapping[str, object], profile: ConnectionProfile) -> SubmissionReceipt:
        """Implement scoped submission and honest, idempotent receipt handling."""
        raise NotImplementedError

    @abstractmethod
    def read_cognition_state(self, receipt: SubmissionReceipt, profile: ConnectionProfile) -> CognitionReceipt:
        """Report unobservable when the Node exposes no matching status API."""
        raise NotImplementedError


class ResearchHook(ABC):
    @abstractmethod
    def assess(self, signals: ResearchSignals, policy: Mapping[str, object]) -> ResearchDecision:
        """Implement gated acquisition suggestions, not fact verification."""
        raise NotImplementedError
