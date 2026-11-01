"""Logical contracts, not Node request schemas or validated runtime policy.

These records neither enforce authorization nor perform I/O. A derived
component must validate input and map to its installed Node's public API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Mapping


@dataclass(frozen=True, kw_only=True)
class AcquisitionRequest:
    source_id: str
    intent: str
    requested_scopes: tuple[str, ...] = ()
    authorization_reference: str | None = None
    cursor: str | None = None
    limit: int = 1


@dataclass(frozen=True, kw_only=True)
class Coverage:
    available_modalities: tuple[str, ...] = ()
    covered_ranges: tuple[str, ...] = ()
    missing_ranges: tuple[str, ...] = ()
    completeness: Literal["complete", "partial", "unknown"] = "unknown"


@dataclass(frozen=True, kw_only=True)
class SourceIdentity:
    source_id: str
    record_id: str
    revision: str
    content_hash: str
    source_role: Literal["author_claim", "user_statement", "tool_observation", "derived_summary"]
    uri: str | None = None
    root_source_id: str | None = None
    locator: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True)
class AcquiredItem:
    source: SourceIdentity
    content: str
    coverage: Coverage
    subject_id: str | None = None
    occurred_at: str | None = None
    recorded_at: str | None = None
    visibility: Literal["private", "public", "unknown"] = "unknown"
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True)
class AcquisitionBatch:
    items: tuple[Mapping[str, object], ...] = ()
    next_cursor: str | None = None
    snapshot_scope: str | None = None
    completeness: Literal["complete", "partial", "unknown"] = "unknown"
    # Absence from a partial batch never implies deletion.
    deletion_markers: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class ConnectionProfile:
    base_url: str | None = None
    api_prefix: str = "/api/v1"
    credential_reference: str | None = None
    bank_id: str | None = None
    authorization_reference: str | None = None


@dataclass(frozen=True, kw_only=True)
class NodeContractReport:
    reachable: bool | None = None
    node_version: str | None = None
    observation_submission_supported: bool | None = None
    source_contract_supported: bool | None = None
    cognitive_status_observable: bool | None = None
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class SubmissionReceipt:
    correlation_id: str
    idempotency_key: str
    observation_id: str | None = None
    transport_state: Literal["not_attempted", "persisted", "rejected", "unknown"] = "not_attempted"
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class CognitionReceipt:
    observation_id: str
    stage: Literal["unobservable", "recorded", "indexed", "candidate", "under_review", "rejected", "unknown"]
    claim_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class ResearchSignals:
    task_relevance: float | None = None
    coverage_gap: float | None = None
    evidence_gap: float | None = None
    contradiction: float | None = None
    staleness: float | None = None
    blocking_gap: bool | None = None
    explicit_research_request: bool = False
    # Values describe acquisition need, never fact confidence.


@dataclass(frozen=True, kw_only=True)
class ResearchDecision:
    action: Literal["blocked", "suggest", "skip", "needs_input"]
    reason_codes: tuple[str, ...] = ()
    public_queries: tuple[str, ...] = ()
    # A suggestion neither authorizes nor executes a search.
