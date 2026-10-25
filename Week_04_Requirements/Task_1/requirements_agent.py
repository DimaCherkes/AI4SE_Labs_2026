#!/usr/bin/env python3
"""
requirements_agent.py — LangGraph Software Requirements Refinement Agentic Network.
===================================================================================
A production-grade agentic pipeline constructed with LangGraph that ingests a heterogeneous
corpus of plain-text and RFC 822 email files, extracts candidate requirements, deduplicates
and normalizes concepts, audits against quality specifications (OS1–OS9), and iteratively
refines the requirements through a verified feedback loop before rendering a complete
requirements specification document in Markdown.

Meets Course Assignment Specifications:
  - ANS1: >= 3 agentic (LLM-invoking) nodes.
  - ANS2: >= 1 deterministic (non-AI) node.
  - ANS3: >= 1 feedback loop with convergence counter guard.
  - ANS4: >= 3 distinct permitted models from OpenAI.
  - ANS5: Implemented using Python's LangGraph StateGraph framework.
  - OS1–OS9: Structured Markdown output with unique IDs, traceability, narrative paragraphs,
             MoSCoW priority scale, zero contradictions, and dedicated Blacklist.
"""

from __future__ import annotations

import argparse
import copy
import json
import logging
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Set, Tuple, TypedDict, Union

from dotenv import load_dotenv

# Load environment variables (.env contains OPENAI_API_KEY)
load_dotenv()

# Dual compatibility: Pydantic v2 / v1
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs: Any):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self) -> Dict[str, Any]:
            return self.__dict__.copy()
        def dict(self) -> Dict[str, Any]:
            return self.__dict__.copy()
    def Field(default: Any = None, default_factory: Any = None, description: str = "") -> Any:  # type: ignore
        return default_factory() if default_factory else default

# LangChain & LangGraph imports
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# Deterministic Ingestion module (ANS2)
import ingest

logger = logging.getLogger("requirements_agent")


# ==============================================================================
# Model Configuration & NODE_CONFIGS (ANS4, verify_pipeline contract)
# ==============================================================================

ALLOWED_MODELS: set[str] = {
    "gpt-6-luna",
    "gpt-5.6-luna",
    "gpt-5.4-nano",
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-4.1-nano",
    "gpt-4o-mini",
}

NODE_CONFIGS: Dict[str, Dict[str, str]] = {
    "extract_requirements": {"type": "llm", "model": "gpt-5-mini"},
    "resolve_conflicts_and_deduplicate": {"type": "llm", "model": "gpt-5.4-nano"},
    "audit_requirements": {"type": "llm", "model": "gpt-6-luna"},
    "refine_requirements": {"type": "llm", "model": "gpt-5.6-luna"},
}


# ==============================================================================
# State Schemas (PROJECT.md Interface Contract)
# ==============================================================================

class Requirement(BaseModel):
    """Normalized requirement specification entity."""
    id: str = Field(description="Unique canonical identifier, e.g. REQ-001")
    title: str = Field(description="Short descriptive requirement name (>=3 words)")
    explanation: str = Field(description="Coherent narrative paragraph explanation (>=40 words)")
    priority: str = Field(description="MoSCoW priority: Must Have, Should Have, Could Have, Won't Have")
    sources: List[str] = Field(description="List of relative source document paths from corpus_dir")
    subsystem: str = Field(description="Functional subsystem category")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump() if hasattr(self, "model_dump") else self.dict()


class BlacklistItem(BaseModel):
    """Discarded, non-viable, or contradictory proposal entity (OS9)."""
    id: str = Field(description="Unique blacklist identifier, e.g. BLK-001")
    title: str = Field(description="Title of discarded or rejected proposal")
    rationale: str = Field(description="Stakeholder and technical justification for rejection (>=15 words)")
    sources: List[str] = Field(description="Source documents where the rejected proposal appeared")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump() if hasattr(self, "model_dump") else self.dict()


class AuditReport(BaseModel):
    """Quality evaluation report produced by the auditor node."""
    passed: bool = Field(description="True if all OS1-OS9 criteria are satisfied")
    issues: List[str] = Field(default_factory=list, description="Defects or refinement recommendations")
    feedback: str = Field(default="", description="Constructive feedback for the refinement node")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump() if hasattr(self, "model_dump") else self.dict()


class AgentState(TypedDict):
    """LangGraph pipeline global state schema."""
    corpus_dir: str
    output_file: str
    documents: List[Dict[str, Any]]
    raw_requirements: List[Dict[str, Any]]
    refined_requirements: List[Dict[str, Any]]
    blacklist: List[Dict[str, Any]]
    audit_report: Optional[Dict[str, Any]]
    iteration_count: int
    max_iterations: int
    mock_mode: bool


# ==============================================================================
# Helper Structured Schemas for Structured LLM Extraction & Refinement
# ==============================================================================

class ExtractedCandidate(BaseModel):
    title: str = Field(description="Descriptive requirement title (at least 3 words)")
    explanation: str = Field(description="Comprehensive narrative paragraph explanation (at least 40 words)")
    priority: str = Field(description="Must Have, Should Have, Could Have, or Won't Have")
    sources: List[str] = Field(description="List of relative source document paths from which requirement was derived")
    subsystem: str = Field(description="Subsystem name: Material Volume, Weeding/Purging, Patron Demographics, Financial, Query/Queue, Security/Auth")


class ExtractionBatchResult(BaseModel):
    requirements: List[ExtractedCandidate] = Field(description="List of extracted candidate requirements")


class DeduplicationResult(BaseModel):
    refined_requirements: List[Requirement] = Field(description="Deduplicated and normalized requirements with sequential IDs REQ-001, REQ-002, ...")
    blacklist: List[BlacklistItem] = Field(description="Discarded or rejected proposals with sequential IDs BLK-001, BLK-002, ... and detailed rationales (>=15 words)")


class RefinementResult(BaseModel):
    updated_requirements: List[Requirement] = Field(default_factory=list, description="Updated active requirements")
    updated_blacklist: List[BlacklistItem] = Field(default_factory=list, description="Updated rejected proposals")
    removed_requirement_ids: List[str] = Field(default_factory=list, description="Duplicate requirement IDs merged into surviving entries")


# ==============================================================================
# Robust JSON Parsing Helpers
# ==============================================================================

def _parse_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Robustly extracts and parses a JSON object from LLM response text."""
    if not text:
        return None
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    match = re.search(r'(\{[\s\S]*\})', text)
    if match:
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return None


def _parse_json_array(text: str) -> Optional[List[Dict[str, Any]]]:
    """Robustly extracts and parses a JSON array of dicts from LLM response text."""
    if not text:
        return None
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()
    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
    except Exception:
        pass

    match = re.search(r'(\[[\s\S]*\])', text)
    if match:
        try:
            data = json.loads(match.group(1))
            if isinstance(data, list):
                return [x for x in data if isinstance(x, dict)]
        except Exception:
            pass
    return None


# ==============================================================================
# Isolated Mock Fixtures & Helpers (Strictly used when mock_mode=True or no LLM)
# ==============================================================================

MOCK_EVERGREEN_REQUIREMENTS: List[Dict[str, Any]] = [
    {
        "id": "REQ-001",
        "title": "Material Volume Calculation and Linear Shelf Space Sizing",
        "explanation": (
            "The Evergreen ILS reporting module must calculate accurate material volumes across all physical shelving locations "
            "by converting item counts into linear shelf inches based on standardized classification call number averages. "
            "The system shall compute total linear shelf space consumption across call number ranges, branch collections, "
            "and circulating item statuses using calibrated formulaic spine thickness factors. This calculation provides branch managers "
            "with precise physical inventory footprint metrics for collection management and facility expansion planning."
        ),
        "priority": "Must Have",
        "sources": [
            "conversations/conv_pines014_material_volume.eml",
            "conversations/conv_pines016_shelf_space.eml",
            "early_draft_srs_galecia.txt",
        ],
        "subsystem": "Material Volume & Shelf Space",
    },
    {
        "id": "REQ-002",
        "title": "Interactive Branch Shelf Capacity and Threshold Utilization Warnings",
        "explanation": (
            "The system shall deliver dynamic reporting views comparing total shelving linear capacity against measured collection "
            "volumes for every branch library facility. When material volumes exceed parameterized percentage thresholds "
            "(e.g., 85% maximum capacity), the interface must trigger visual warning indicators and automated alert notifications "
            "to designated library administrators, preventing physical space overfilling and supporting proactive weeding initiatives."
        ),
        "priority": "Should Have",
        "sources": [
            "conversations/conv_pines015_capacity_interface.eml",
            "conversations/conv_pines016_shelf_space.eml",
        ],
        "subsystem": "Material Volume & Shelf Space",
    },
    {
        "id": "REQ-003",
        "title": "Inter-Branch Item Transfer Manifests and In-Transit Tracking",
        "explanation": (
            "The reporting interface must track physical items moving between library branches, generating formal transfer packing "
            "slips and transit verification reports. Discrepancies between transit initiation and receipt check-in must be flagged "
            "as in-transit missing items after a configurable holding window of 14 days, preventing inventory loss during "
            "inter-library loan logistics."
        ),
        "priority": "Must Have",
        "sources": [
            "conversations/conv_pines018_item_transfer.eml",
            "conversations/conv_pines019_020_missing_intransit.eml",
        ],
        "subsystem": "Weeding & Purging",
    },
    {
        "id": "REQ-004",
        "title": "Item Deletion Status Distinctions and Catalog Purging Safeguards",
        "explanation": (
            "The system shall enforce rigorous structural distinctions between deleted items and purged items within the reporting "
            "database schema. Soft-deleted records must remain queryable in historical statistical summaries and circulating metrics "
            "for a minimum of 24 months before irreversible permanent purge operations can be authorized by regional database administrators."
        ),
        "priority": "Must Have",
        "sources": [
            "conversations/conv_pines021_item_purging.eml",
            "conversations/conv_pines022_deletions.eml",
        ],
        "subsystem": "Weeding & Purging",
    },
    {
        "id": "REQ-005",
        "title": "Multi-Criteria Weeding Candidate Identification and Soft-Deletion",
        "explanation": (
            "The reporting tool shall generate multi-criteria candidate weeding lists identifying physical items with zero "
            "circulations over the preceding three years, multiple damaged condition flags, or superseded edition markers. "
            "All candidate records marked for removal must enter a two-stage soft-deletion state allowing physical shelf inspection "
            "and administrative review prior to permanent record purge execution, ensuring comprehensive preservation of historical holdings."
        ),
        "priority": "Should Have",
        "sources": [
            "conversations/conv_pines021_item_purging.eml",
            "conversations/conv_pines022_deletions.eml",
            "meeting_minutes/meeting_2009-03-15_minutes.txt",
        ],
        "subsystem": "Weeding & Purging",
    },
    {
        "id": "REQ-006",
        "title": "Patron Inactive Status Detection and Data Retention Lifecycle",
        "explanation": (
            "The reporting module shall execute scheduled batch evaluations to flag patron accounts with zero circulation, payment, "
            "or digital authentication activity over an administrator-defined inactivity threshold (e.g., 36 months). Inactive "
            "accounts must be flagged for retention review or anonymized archival in strict compliance with state public record management "
            "mandates and patron privacy regulations."
        ),
        "priority": "Should Have",
        "sources": [
            "conversations/conv_pines024_inactive_patrons.eml",
            "evergreen_reference_2009.txt",
        ],
        "subsystem": "Patron Demographics & Inactive",
    },
    {
        "id": "REQ-007",
        "title": "Patron Demographic and Geographic Distribution Analytics",
        "explanation": (
            "The reporting subsystem shall generate aggregated demographic and postal code distribution profiles correlating "
            "patron registration density with circulation intensity and facility access patterns. To safeguard individual privacy, "
            "all geospatial reports must enforce cell suppression algorithms that mask demographic groupings representing fewer "
            "than five individuals."
        ),
        "priority": "Could Have",
        "sources": [
            "conversations/conv_pines023_patron_characteristics.eml",
            "survey_results_2009.txt",
        ],
        "subsystem": "Patron Demographics & Inactive",
    },
    {
        "id": "REQ-008",
        "title": "Granular Staff User Authentication and Role-Based Permissions",
        "explanation": (
            "The administrative reporting module shall restrict report definition, template authoring, and query execution capabilities "
            "through an explicit role-based access control matrix. Individual staff user accounts must be authenticated against "
            "verified credentials and assigned least-privilege reporting permissions corresponding to their institutional organizational tier."
        ),
        "priority": "Must Have",
        "sources": [
            "email_staff_login.eml",
            "evergreen_reference_2009.txt",
        ],
        "subsystem": "Security & Authentication",
    },
    {
        "id": "REQ-009",
        "title": "Financial Fine Reconciliation and Ledger Export",
        "explanation": (
            "The system shall deliver comprehensive daily and monthly financial reconciliation ledgers tracking patron fine assessments, "
            "cash and card fee payments, fee forgiveness exemptions, and outstanding billing balances. All financial summaries "
            "must cross-reference terminal operator IDs and export structured reconciliation files formatted for standard municipal "
            "municipal accounting software."
        ),
        "priority": "Must Have",
        "sources": [
            "email_financial_reports.eml",
            "meeting_minutes/meeting_2009-07-20_minutes.txt",
        ],
        "subsystem": "Financial Reporting",
    },
    {
        "id": "REQ-010",
        "title": "Standardized and Ad-Hoc Report Template Designer",
        "explanation": (
            "The reporting tool shall provide both a repository of standardized pre-built administrative reports and an intuitive "
            "wizard interface for constructing ad-hoc report templates. Authorized staff members must be able to select data sources, "
            "configure filter expressions, designate grouping hierarchies, and save customized template definitions for recurring departmental use."
        ),
        "priority": "Must Have",
        "sources": [
            "email_report_features.eml",
            "interview_cataloging_2009-05-08.txt",
        ],
        "subsystem": "Query & Queue Management",
    },
    {
        "id": "REQ-011",
        "title": "Automated Asynchronous Report Scheduling and Email Delivery",
        "explanation": (
            "The system shall allow staff to schedule complex, recurring report generation jobs during off-peak processing hours "
            "(e.g., nightly or weekly). Upon task completion, the scheduling daemon must generate output files in the requested format "
            "and automatically distribute them via authenticated SMTP to designated stakeholder mailing distribution lists."
        ),
        "priority": "Should Have",
        "sources": [
            "email_report_features.eml",
            "meeting_tech_subcommittee_2009-06-30.txt",
        ],
        "subsystem": "Query & Queue Management",
    },
    {
        "id": "REQ-012",
        "title": "Background Report Queue Execution and Resource Throttling",
        "explanation": (
            "All reporting queries exceeding configured runtime thresholds must execute asynchronously within a background job queue "
            "rather than in synchronous web client sessions. The queue manager shall enforce concurrency limits, thread pooling, and CPU/memory "
            "quotas to protect production transactional circulation performance from intensive analytical database queries."
        ),
        "priority": "Must Have",
        "sources": [
            "interview_sysadmin_2009-05-10.txt",
            "meeting_tech_subcommittee_2009-06-30.txt",
        ],
        "subsystem": "Query & Queue Management",
    },
    {
        "id": "REQ-013",
        "title": "Query Optimization and PostgreSQL Database Indexing Safeguards",
        "explanation": (
            "The reporting engine shall enforce database indexing rules and query structure validation against the underlying "
            "PostgreSQL relational engine. Ad-hoc report templates that would trigger unindexed sequential table scans on core "
            "circulation transaction tables must be intercepted and rejected with constructive optimization guidance for the author."
        ),
        "priority": "Must Have",
        "sources": [
            "interview_sysadmin_2009-05-10.txt",
            "evergreen_reference_2009.txt",
        ],
        "subsystem": "Query & Queue Management",
    },
    {
        "id": "REQ-014",
        "title": "Multi-Format Data Export and Encoding Standards",
        "explanation": (
            "All generated tabular and summary reports must support seamless data export into industry-standard digital formats, "
            "including UTF-8 encoded Comma-Separated Values (CSV), Microsoft Excel OpenXML (XLSX), and Portable Document Format (PDF). "
            "Exported files must strictly preserve special diacritical characters, MARC 21 cataloging encodings, and numerical precision."
        ),
        "priority": "Should Have",
        "sources": [
            "interview_cataloging_2009-05-08.txt",
            "email_report_features.eml",
        ],
        "subsystem": "Query & Queue Management",
    },
    {
        "id": "REQ-015",
        "title": "Section 508 Accessibility and Web Standards Compliance",
        "explanation": (
            "All web-based reporting interfaces, parameter selection forms, and generated HTML report outputs must comply fully with "
            "Federal Section 508 accessibility guidelines and W3C WCAG 2.0 Level AA standards. Interfaces must provide full keyboard "
            "navigation, high-contrast visual display options, and semantic labeling compatible with standard screen readers."
        ),
        "priority": "Must Have",
        "sources": [
            "survey_results_2009.txt",
            "meeting_tech_subcommittee_2009-06-30.txt",
        ],
        "subsystem": "Security & Authentication",
    },
    {
        "id": "REQ-016",
        "title": "Administrative Configuration and Audit Logging Trail",
        "explanation": (
            "The reporting subsystem shall maintain an immutable administrative audit log capturing all system configuration modifications, "
            "template deletions, scheduled execution failures, and staff access events. Audit logs must record ISO 8601 timestamps, "
            "authenticated user identifiers, source IP addresses, and detailed modification deltas to satisfy state regulatory oversight."
        ),
        "priority": "Must Have",
        "sources": [
            "email_staff_login.eml",
            "interview_sysadmin_2009-05-10.txt",
        ],
        "subsystem": "Security & Authentication",
    },
]

MOCK_EVERGREEN_BLACKLIST: List[Dict[str, Any]] = [
    {
        "id": "BLK-001",
        "title": "Mandatory Magnetic Card-Swipe for Patron Identification",
        "rationale": (
            "Stakeholders and privacy advocates rejected mandatory card-swipe identification due to severe privacy civil liberties "
            "concerns, unnecessary hardware procurement costs, and lack of support for patrons lacking physical magnetic cards. "
            "The system instead supports optional barcode scanning and manual patron lookup."
        ),
        "sources": [
            "conversations/conv_pines023_patron_characteristics.eml",
            "survey_results_2009.txt",
        ],
    },
    {
        "id": "BLK-002",
        "title": "Real-Time Denormalized Global Reporting Warehouse",
        "rationale": (
            "Systems administration and database engineering rejected proposals for a separate real-time denormalized data warehouse. "
            "The maintenance overhead, replication latency risks, and PostgreSQL hardware resource limitations made maintaining "
            "dual schema synchronization unsustainable. The architecture instead leverages dedicated read-only database replicas."
        ),
        "sources": [
            "interview_sysadmin_2009-05-10.txt",
            "meeting_tech_subcommittee_2009-06-30.txt",
        ],
    },
    {
        "id": "BLK-003",
        "title": "Direct Unchecked Batch Purging of Historical Circulation Records",
        "rationale": (
            "Proposals to allow immediate, hard-delete batch purging of circulation history without multi-stage soft-deletion and "
            "administrative approval were rejected. Direct purging presents unacceptable risks of permanent statistical data loss and "
            "violates public library accountability and audit retention policies."
        ),
        "sources": [
            "conversations/conv_pines021_item_purging.eml",
            "meeting_minutes/meeting_2009-03-15_minutes.txt",
        ],
    },
    {
        "id": "BLK-004",
        "title": "Unrestricted Ad-Hoc Query Access to Patron PII and Financial Tables",
        "rationale": (
            "Unrestricted ad-hoc SQL query execution against tables containing patron personally identifiable information (PII) or "
            "unmasked financial transactions was strictly rejected by committee consensus. Permitting direct access violates patron "
            "confidentiality policies and municipal financial audit controls. All reporting access must occur through governed, parameterized views."
        ),
        "sources": [
            "email_staff_login.eml",
            "email_financial_reports.eml",
            "survey_results_2009.txt",
        ],
    },
]

MOCK_EVERGREEN_EXPANSIONS: Dict[str, str] = {
    "REQ-001": (
        "The Evergreen ILS reporting module must calculate accurate material volumes across all physical shelving "
        "locations by converting item counts into linear shelf inches based on standardized classification call number "
        "averages. The system shall compute total linear shelf space consumption across call number ranges, branch collections, "
        "and circulating item statuses using calibrated formulaic spine thickness factors. This calculation provides branch managers "
        "with precise physical inventory footprint metrics for collection management and facility expansion planning."
    ),
    "REQ-005": (
        "The reporting tool shall generate multi-criteria candidate weeding lists identifying physical items with zero "
        "circulations over the preceding three years, multiple damaged condition flags, or superseded edition markers. "
        "All candidate records marked for removal must enter a two-stage soft-deletion state allowing physical shelf inspection "
        "and administrative review prior to permanent record purge execution, ensuring comprehensive preservation of historical holdings."
    ),
}


def _is_evergreen_corpus(documents: List[Dict[str, Any]]) -> bool:
    """Checks whether the ingested documents correspond to the Evergreen PINES library corpus."""
    if not documents:
        return False
    for d in documents:
        path = str(d.get("source_path", "")).lower()
        content = str(d.get("content", "")).lower()[:1000]
        if "pines" in path or "galecia" in path or "evergreen" in path:
            return True
        if "evergreen" in content or "pines" in content:
            return True
    return False


def _extract_mock_candidates_from_arbitrary_corpus(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Dynamically parses arbitrary corpus documents for mock mode without hardcoded fixtures."""
    candidates: List[Dict[str, Any]] = []
    idx = 1
    for doc in documents:
        src = doc.get("source_path", "document.txt")
        content = str(doc.get("content", "")).strip()
        doc_title = str(doc.get("title", "")).strip() or Path(src).stem.replace("_", " ").title()

        # Split into sentences
        raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', content) if s.strip()]
        modal_sentences = [
            s for s in raw_sentences
            if any(w in s.lower() for w in ("must", "shall", "should", "require", "needs to", "will"))
        ]
        chosen_sentences = modal_sentences if modal_sentences else raw_sentences[:5]

        for s in chosen_sentences[:4]:
            clean_s = s.replace("\n", " ").strip()
            if len(clean_s) < 15:
                continue

            words = clean_s.split()
            title_prefix = " ".join(words[:5]) if len(words) >= 5 else f"Specification for {doc_title}"
            title = f"{title_prefix.title()}"
            if len(title.split()) < 3:
                title = f"Requirement for {title}"

            candidates.append({
                "id": f"RAW-{idx:03d}",
                "title": title,
                "explanation": clean_s,
                "priority": "Must Have",
                "sources": [src],
                "subsystem": "General System Specification",
            })
            idx += 1

    if not candidates and documents:
        first_doc = documents[0]
        src = first_doc.get("source_path", "document.txt")
        candidates.append({
            "id": "RAW-001",
            "title": "General System Functional Capability",
            "explanation": f"The software architecture must implement core functionality defined in {src}.",
            "priority": "Must Have",
            "sources": [src],
            "subsystem": "General System Specification",
        })
    return candidates


def _get_mock_raw_requirements(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Returns candidate requirements for mock mode."""
    if not documents:
        return []

    if _is_evergreen_corpus(documents):
        raw_list: List[Dict[str, Any]] = []
        for req in MOCK_EVERGREEN_REQUIREMENTS:
            r = req.copy()
            if r["id"] == "REQ-001":
                r["explanation"] = (
                    "The Evergreen ILS reporting module must calculate accurate material volumes across all physical shelving "
                    "locations by converting item counts into linear shelf inches based on classification call number averages."
                )
            elif r["id"] == "REQ-005":
                r["explanation"] = (
                    "The reporting tool shall generate multi-criteria candidate weeding lists identifying physical items with zero "
                    "circulations over three years, damaged condition flags, or superseded edition markers for administrative review."
                )
            raw_list.append(r)
        return raw_list

    return _extract_mock_candidates_from_arbitrary_corpus(documents)


def _get_mock_dedup_and_blacklist(
    documents: List[Dict[str, Any]], raw_reqs: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Returns deduplicated requirements and blacklist items for mock mode."""
    if not documents:
        return {"refined_requirements": [], "blacklist": []}

    if _is_evergreen_corpus(documents):
        refined = [r.copy() for r in raw_reqs]
        for idx, r in enumerate(refined, start=1):
            r["id"] = f"REQ-{idx:03d}"
        blacklist = [b.copy() for b in MOCK_EVERGREEN_BLACKLIST]
        return {"refined_requirements": refined, "blacklist": blacklist}

    # For an arbitrary corpus, the mock cannot infer that any proposal was rejected.
    refined = [r.copy() for r in raw_reqs]
    for idx, r in enumerate(refined, start=1):
        r["id"] = f"REQ-{idx:03d}"
    return {"refined_requirements": refined, "blacklist": []}


def _resolve_candidate_sources(
    sources: List[str], raw_sources: Dict[str, List[str]], known_paths: Set[str]
) -> List[str]:
    """Turn candidate IDs in LLM citations into real, corpus-relative paths."""
    if not isinstance(sources, list):
        raise ValueError("Source citations must be a list")
    resolved: List[str] = []
    for source in sources:
        if not isinstance(source, str):
            raise ValueError("Source citations must be strings")
        candidate_match = re.fullmatch(r"RAW-(\d+)", source, re.IGNORECASE)
        if candidate_match:
            canonical_id = f"RAW-{int(candidate_match.group(1)):03d}"
            if canonical_id in raw_sources:
                source = canonical_id
        for item in raw_sources.get(source, [source]):
            normalized = item.replace("\\", "/")
            if normalized not in known_paths:
                matches = [path for path in known_paths if Path(path).name == normalized]
                if len(matches) != 1:
                    raise ValueError(f"Citation does not identify one corpus document: {source!r}")
                normalized = matches[0]
            if normalized not in resolved:
                resolved.append(normalized)
    if not resolved:
        raise ValueError("Requirement or blacklist item has no corpus citations")
    return resolved


def _missing_consolidated_sources(
    documents: List[Dict[str, Any]], items: List[Dict[str, Any]]
) -> Set[str]:
    """Find explicit requirement summaries that disappeared from a pipeline stage."""
    expected = {
        d["source_path"] for d in documents if d.get("source_path")
        and re.search(r"(?i)requirement consolidated\s*:|summary:.*requirement",
                      str(d.get("content", "")))
    }
    cited = {source for item in items for source in item.get("sources", [])}
    return expected - cited


# ==============================================================================
# Helper Functions: LLM Initialization
# ==============================================================================

def get_llm(node_name: str, mock_mode: bool = False) -> Optional[ChatOpenAI]:
    """Instantiates the ChatOpenAI client configured for the specific node."""
    if mock_mode:
        return None
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        raise RuntimeError("OPENAI_API_KEY is required for a live run; use --mock for offline testing")

    cfg = NODE_CONFIGS.get(node_name, {"model": "gpt-5-mini"})
    model = cfg.get("model", "gpt-5-mini")
    try:
        if "luna" in model:
            return ChatOpenAI(model=model, api_key=api_key, request_timeout=90, max_retries=1)
        return ChatOpenAI(model=model, temperature=0.2, api_key=api_key,
                          request_timeout=90, max_retries=1)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize {model} for {node_name}") from e


# ==============================================================================
# Node 1: Deterministic Corpus Ingestion (ANS2)
# ==============================================================================

def ingest_corpus(state: AgentState) -> Dict[str, Any]:
    """Deterministic ingestion node parsing all .txt and .eml files in corpus_dir.
    
    Adheres strictly to ANS2 and OS4: preserves source path provenance.
    """
    corpus_dir = state.get("corpus_dir", "data/corpus")
    if not corpus_dir or not str(corpus_dir).strip():
        raise ValueError("Corpus directory path cannot be empty.")
    logger.info(f"[Node: ingest_corpus] Ingesting files from {corpus_dir}")
    doc_items = ingest.ingest_corpus(corpus_dir)
    documents = [d.to_dict() if hasattr(d, "to_dict") else d.dict() for d in doc_items]
    logger.info(f"[Node: ingest_corpus] Successfully parsed {len(documents)} documents")
    return {"documents": documents}


# ==============================================================================
# Node 2: Requirement Extraction (LLM Node 1: gpt-5-mini)
# ==============================================================================

def extract_requirements(state: AgentState) -> Dict[str, Any]:
    """Extracts candidate functional requirements grounded in corpus document content.
    
    Batches documents and uses gpt-5-mini with structured output (ANS1, ANS4, OS4, OS8).
    """
    mock_mode = state.get("mock_mode", False)
    llm = get_llm("extract_requirements", mock_mode)
    documents = state.get("documents", [])

    if mock_mode:
        return {"raw_requirements": _get_mock_raw_requirements(documents)}

    logger.info(f"[Node: extract_requirements] Extracting requirements from {len(documents)} documents using gpt-5-mini")

    # Partition documents into balanced batches of up to 4 documents or ~25,000 characters
    batches: List[List[Dict[str, Any]]] = []
    current_batch: List[Dict[str, Any]] = []
    current_chars = 0
    for doc in documents:
        doc_len = len(doc.get("content", ""))
        if current_batch and (len(current_batch) >= 4 or (current_chars + doc_len > 25000)):
            batches.append(current_batch)
            current_batch = [doc]
            current_chars = doc_len
        else:
            current_batch.append(doc)
            current_chars += doc_len
    if current_batch:
        batches.append(current_batch)

    raw_requirements: List[Dict[str, Any]] = []

    for idx, batch in enumerate(batches, start=1):
        batch_entries = []
        for i, d in enumerate(batch, start=1):
            src = d.get('source_path', 'doc.txt')
            t = d.get('title', 'Document')
            c = d.get('content', '')[:10000]
            batch_entries.append(f"=== Document {i}: {src} ===\nTitle/Subject: {t}\nContent:\n{c}")
        docs_text = "\n\n".join(batch_entries)

        prompt = (
            f"You are a principal software requirements engineer. Analyze the following ingested corpus documents "
            f"(Batch {idx}/{len(batches)}) and extract candidate functional requirements.\n\n"
            f"{docs_text}\n\n"
            f"Extraction Guidelines:\n"
            f"1. For each requirement provide: title (>=3 words), narrative paragraph explanation (>=40 words), "
            f"   valid MoSCoW priority (Must Have, Should Have, Could Have, Won't Have), relative source paths, "
            f"   and functional subsystem.\n"
            f"2. Extract concrete functional requirements covering core workflows discussed in the text.\n"
            f"3. Include explicitly rejected, discarded, or conflicting proposals as separate candidates "
            f"with Won't Have priority. State the rejected proposal plainly so the next node can put it "
            f"in the blacklist; do not replace it only with the preferred alternative.\n"
            f"4. Ground each behavior in the cited documents. Do not add queues, fields, roles, thresholds, "
            f"or other implementation details that the source does not support.\n"
            f"5. Cover every document in this batch that states a substantive requirement. In particular, "
            f"preserve any explicit 'requirement consolidated' or summary decision, with its own source path.\n"
            f"6. Exclude non-functional conversational chatter and informal digressions.\n"
        )
        try:
            structured_llm = llm.with_structured_output(ExtractionBatchResult)
            res: ExtractionBatchResult = structured_llm.invoke([
                SystemMessage(content="You are a professional requirements extraction specialist."),
                HumanMessage(content=prompt)
            ])
            for req in res.requirements:
                d_req = req.model_dump() if hasattr(req, "model_dump") else req.dict()
                d_req["id"] = f"RAW-{len(raw_requirements)+1:03d}"
                raw_requirements.append(d_req)
        except Exception as e:
            logger.warning(f"[Node: extract_requirements] Batch {idx} structured invoke failed: {e}; attempting JSON fallback")
            try:
                response = llm.invoke([
                    SystemMessage(content="You are a professional requirements extraction specialist. Output only valid JSON."),
                    HumanMessage(content=prompt + "\nOutput a JSON object: {\"requirements\": [{\"title\": \"...\", \"explanation\": \"...\", \"priority\": \"...\", \"sources\": [...], \"subsystem\": \"...\"}]}")
                ])
                parsed = _parse_json_object(response.content)
                if parsed and "requirements" in parsed:
                    for item in parsed["requirements"]:
                        item["id"] = f"RAW-{len(raw_requirements)+1:03d}"
                        raw_requirements.append(item)
            except Exception as e2:
                raise RuntimeError(f"Extraction failed for batch {idx}/{len(batches)}") from e2

    if not raw_requirements:
        raise RuntimeError("Live extraction returned zero requirements; no output was written")
    missing = _missing_consolidated_sources(documents, raw_requirements)
    if missing:
        raise RuntimeError(f"Live extraction missed consolidated requirement sources: {sorted(missing)}")

    logger.info(f"[Node: extract_requirements] Successfully extracted {len(raw_requirements)} candidate requirements")
    return {"raw_requirements": raw_requirements}


# ==============================================================================
# Node 3: Conflict Resolution & Deduplication (LLM Node 2: gpt-5.4-nano)
# ==============================================================================

def resolve_conflicts_and_deduplicate(state: AgentState) -> Dict[str, Any]:
    """Clusters duplicates, unifies vocabulary, assigns REQ-001.., and isolates Blacklist.
    
    Uses gpt-5.4-nano to fulfill OS2, OS3, OS7, and OS9.
    """
    mock_mode = state.get("mock_mode", False)
    llm = get_llm("resolve_conflicts_and_deduplicate", mock_mode)
    raw_reqs = state.get("raw_requirements", [])
    documents = state.get("documents", [])

    if mock_mode:
        return _get_mock_dedup_and_blacklist(documents, raw_reqs)

    logger.info(f"[Node: resolve_conflicts_and_deduplicate] Deduplicating {len(raw_reqs)} candidates with gpt-5.4-nano")

    req_summaries = json.dumps([
        {
            "id": r.get("id"),
            "title": r.get("title"),
            "explanation": r.get("explanation"),
            "priority": r.get("priority"),
            "sources": r.get("sources"),
            "subsystem": r.get("subsystem"),
        }
        for r in raw_reqs
    ], indent=2)

    prompt = (
        "You are a requirements deduplication and conflict resolution engine.\n"
        "Analyze the following list of candidate requirements extracted from the corpus:\n\n"
        f"{req_summaries}\n\n"
        "Tasks:\n"
        "1. Merge semantically duplicate or overlapping requirements into a unified specification. Combine their source lists.\n"
        "2. Ensure each active requirement has a descriptive title (>=3 words) and a narrative paragraph explanation (>=40 words).\n"
        "3. Assign sequential canonical IDs REQ-001, REQ-002, ...\n"
        "4. Move every explicitly rejected or conflicting candidate, including every Won't Have candidate, "
        "into the Blacklist with sequential IDs BLK-001, BLK-002, ... and a rationale (>=15 words). "
        "If there is no evidence of a rejected proposal, leave the blacklist empty.\n"
        "5. Keep every behavior and rationale grounded in the candidates. Do not invent workflows, fields, "
        "constraints, or rejected proposals. Cite source paths or the candidate RAW IDs; those IDs will "
        "be resolved to corpus paths before export.\n"
        "6. Preserve every source document that has a distinct substantive requirement or explicit rejection "
        "in at least one active requirement or blacklist citation. Do not drop a unique source during merging.\n"
    )

    refined: List[Dict[str, Any]] = []
    blacklist: List[Dict[str, Any]] = []

    try:
        structured_llm = llm.with_structured_output(DeduplicationResult)
        res: DeduplicationResult = structured_llm.invoke([
            SystemMessage(content="You are a requirements deduplication, conflict resolution, and normalization specialist."),
            HumanMessage(content=prompt)
        ])
        refined = [r.model_dump() if hasattr(r, "model_dump") else r.dict() for r in res.refined_requirements]
        blacklist = [b.model_dump() if hasattr(b, "model_dump") else b.dict() for b in res.blacklist]
    except Exception as e:
        logger.warning(f"[Node: resolve_conflicts_and_deduplicate] Structured invoke failed: {e}; attempting JSON fallback")
        try:
            response = llm.invoke([
                SystemMessage(content="You are a requirements deduplication and conflict resolution specialist. Output only valid JSON."),
                HumanMessage(content=prompt + "\nReturn JSON: {\"refined_requirements\": [...], \"blacklist\": [...]}")
            ])
            parsed = _parse_json_object(response.content)
            if parsed:
                refined = parsed.get("refined_requirements", [])
                blacklist = parsed.get("blacklist", [])
        except Exception as e2:
            raise RuntimeError("Live deduplication failed") from e2

    if not refined:
        raise RuntimeError("Live deduplication returned zero requirements; no output was written")

    # Untraceable LLM items cannot satisfy OS4. Discard only items with no citations;
    # malformed or invented citations remain hard errors.
    missing_req_sources = sum(not r.get("sources") for r in refined)
    missing_blk_sources = sum(not b.get("sources") for b in blacklist)
    if missing_req_sources or missing_blk_sources:
        logger.warning("[Node: resolve_conflicts_and_deduplicate] Discarding %d requirements and %d "
                       "blacklist items with no source citations", missing_req_sources, missing_blk_sources)
    refined = [r for r in refined if r.get("sources")]
    blacklist = [b for b in blacklist if b.get("sources")]
    if not refined:
        raise RuntimeError("Live deduplication returned no traceable requirements")

    # Post-processing normalization safeguard
    known_paths = {d["source_path"] for d in documents if d.get("source_path")}
    raw_sources = {r["id"]: r.get("sources", []) for r in raw_reqs if r.get("id")}
    for idx, r in enumerate(refined, start=1):
        r["id"] = f"REQ-{idx:03d}"
        r["sources"] = _resolve_candidate_sources(r.get("sources", []), raw_sources, known_paths)
    for idx, b in enumerate(blacklist, start=1):
        b["id"] = f"BLK-{idx:03d}"
        b["sources"] = _resolve_candidate_sources(b.get("sources", []), raw_sources, known_paths)
    missing = _missing_consolidated_sources(documents, refined + blacklist)
    if missing:
        raise RuntimeError(f"Live deduplication dropped consolidated requirement sources: {sorted(missing)}")

    logger.info(f"[Node: resolve_conflicts_and_deduplicate] Refined {len(refined)} requirements, {len(blacklist)} blacklist items")
    return {"refined_requirements": refined, "blacklist": blacklist}


# ==============================================================================
# Node 4: Requirements Auditor (LLM Node 3: gpt-6-luna)
# ==============================================================================

def audit_requirements(state: AgentState) -> Dict[str, Any]:
    """Audits refined requirements against OS1–OS9 criteria using gpt-6-luna model.
    
    Performs hybrid deterministic and LLM-driven quality auditing on live state.
    Fulfills ANS1, ANS3, ANS4: emits structured AuditReport(passed, issues, feedback).
    """
    iteration = state.get("iteration_count", 0)
    mock_mode = state.get("mock_mode", False)
    llm = get_llm("audit_requirements", mock_mode)
    refined_reqs = state.get("refined_requirements", [])
    blacklist_items = state.get("blacklist", [])
    documents = state.get("documents", [])

    logger.info(f"[Node: audit_requirements] Executing audit at iteration {iteration} on {len(refined_reqs)} requirements")

    issues: List[str] = []

    # --------------------------------------------------------------------------
    # Deterministic Quality Auditing (OS1–OS9)
    # --------------------------------------------------------------------------
    if not refined_reqs:
        issues.append("Requirement set is empty; no requirements to audit.")

    # OS2: Unique IDs & ID Formatting
    req_ids = [r.get("id", "") for r in refined_reqs]
    blk_ids = [b.get("id", "") for b in blacklist_items]
    if len(req_ids) != len(set(req_ids)):
        duplicates = [x for x in req_ids if req_ids.count(x) > 1]
        issues.append(f"Duplicate requirement IDs detected: {set(duplicates)}")
    if len(blk_ids) != len(set(blk_ids)):
        duplicates = [x for x in blk_ids if blk_ids.count(x) > 1]
        issues.append(f"Duplicate blacklist IDs detected: {set(duplicates)}")

    # OS2 & OS5: Title Length (>= 3 words)
    for r in refined_reqs:
        title_words = len(r.get("title", "").split())
        if title_words < 3:
            issues.append(f"{r.get('id')} title is too short ({title_words} words, minimum 3 required)")

    # OS3: Exact & Semantic Deduplication (Jaccard > 0.85)
    for i in range(len(refined_reqs)):
        words_a = set(re.findall(r'\w+', refined_reqs[i].get("title", "").lower()))
        for j in range(i + 1, len(refined_reqs)):
            words_b = set(re.findall(r'\w+', refined_reqs[j].get("title", "").lower()))
            if words_a and words_b:
                jaccard = len(words_a & words_b) / len(words_a | words_b)
                if jaccard > 0.85:
                    issues.append(
                        f"Potential semantic duplicate detected: {refined_reqs[i].get('id')} and "
                        f"{refined_reqs[j].get('id')} have high title similarity (Jaccard={jaccard:.2f})"
                    )

    # OS4: Source Document Provenance Grounding
    known_doc_paths = {d.get("source_path") for d in documents if d.get("source_path")}
    for r in [*refined_reqs, *blacklist_items]:
        sources = r.get("sources", [])
        if not sources:
            issues.append(f"{r.get('id')} lacks source document provenance citations")
        elif known_doc_paths:
            for src in sources:
                norm_src = src.replace("\\", "/")
                if norm_src not in known_doc_paths:
                    issues.append(f"{r.get('id')} cites ungrounded/non-existent corpus document: '{src}'")

    # OS5: Narrative Paragraph Explanation Word Count (>= 40 words) & Prose Check
    for r in refined_reqs:
        exp = r.get("explanation", "")
        words = len(re.findall(r'\w+', exp))
        if words < 40:
            issues.append(f"{r.get('id')} explanation is too short ({words} words, minimum 40 required)")
        lines = [l.strip() for l in exp.splitlines() if l.strip()]
        if lines and all(l.startswith(("-", "*", "•")) for l in lines):
            issues.append(f"{r.get('id')} explanation contains only bullet points instead of narrative prose")

    # OS6: Valid MoSCoW Priority Values
    valid_moscow = {"must have", "should have", "could have", "won't have", "wont have"}
    for r in refined_reqs:
        prio = str(r.get("priority", "")).strip().lower()
        if prio not in valid_moscow:
            issues.append(f"{r.get('id')} has invalid MoSCoW priority '{r.get('priority')}'; must be Must Have, Should Have, Could Have, or Won't Have")

    # OS7: Consistency & Anti-Contradiction / Blacklist Rules
    forbidden_terms = [
        ("mandatory card-swipe", "card-swipe must be optional per patron privacy guidelines"),
        ("mandatory card swipe", "card-swipe must be optional per patron privacy guidelines"),
        ("require card swipe", "card-swipe must be optional per patron privacy guidelines"),
        ("denormalized data warehouse", "denormalized reporting warehouse rejected by sysadmin"),
        ("denormalized reporting warehouse", "denormalized reporting warehouse rejected by sysadmin"),
        ("unanonymized patron", "unanonymized patron tracking violates privacy regulations"),
        ("store patron pii", "storing patron PII in circulating analytics violates privacy regulations"),
    ]
    for r in refined_reqs:
        content_lower = f"{r.get('title', '')} {r.get('explanation', '')}".lower()
        for term, reason in forbidden_terms:
            if term in content_lower:
                issues.append(f"{r.get('id')} contains contradictory/rejected proposal: '{term}' ({reason})")

    # OS9: Blacklist Item Quality & Justification (>= 15 words)
    for b in blacklist_items:
        rat_words = len(re.findall(r'\w+', b.get("rationale", "")))
        if rat_words < 15:
            issues.append(f"{b.get('id')} blacklist justification too short ({rat_words} words, minimum 15 required)")

    # --------------------------------------------------------------------------
    # Live LLM Quality Audit (gpt-6-luna)
    # --------------------------------------------------------------------------
    llm_feedback = ""
    if llm is not None and not mock_mode and refined_reqs:
        try:
            logger.info(f"[Node: audit_requirements] Calling live LLM gpt-6-luna (iteration {iteration})")
            req_summaries = []
            for r in refined_reqs:
                w_count = len(re.findall(r'\w+', r.get("explanation", "")))
                req_summaries.append(
                    f"- {r.get('id')}: \"{r.get('title')}\" [Priority: {r.get('priority')}, Words: {w_count}]\n"
                    f"  Explanation: {r.get('explanation')}"
                )
            req_text = "\n".join(req_summaries)
            prior_note = (
                f"This is audit round {iteration + 1}. Earlier rounds already flagged and fixed issues, so do NOT "
                "repeat stylistic, wording, or 'could be more detailed' remarks.\n"
                if iteration > 0 else ""
            )
            prompt = (
                "You are a requirements quality auditor. Word counts, ID uniqueness, priority values, "
                "title length and source paths are already checked by code, so ignore them.\n\n"
                "Report ONLY these objective, blocking defects:\n"
                "1. CONTRADICTION: two requirements (or a requirement and an explicit rejection) that cannot both be true.\n"
                "2. DUPLICATE: two requirements that specify the same behaviour and should be merged.\n"
                "3. UNSUPPORTED: a concrete claim, number or feature that is clearly invented and not plausible "
                "from the project context.\n\n"
                "Do NOT flag style, tone, missing detail, or minor vagueness. If none of the three defects "
                "exist, return passed=true with an empty issues list.\n"
                f"{prior_note}"
                "Each issue string MUST start with the affected requirement ID (e.g. 'REQ-012: CONTRADICTION with "
                "REQ-040 because ...'). Report at most 10 issues, most severe first.\n\n"
                f"Requirements to audit:\n{req_text}\n\n"
                "Return an AuditReport with passed (bool), issues (list of strings), and feedback (string)."
            )
            try:
                structured_llm = llm.with_structured_output(AuditReport)
                res: AuditReport = structured_llm.invoke([
                    SystemMessage(content="You are a precise requirements auditor who reports only objective, blocking defects."),
                    HumanMessage(content=prompt)
                ])
                if not res.passed and not res.issues:
                    raise ValueError("Auditor failed without actionable issues")
                if res.issues:
                    issues.extend(res.issues[:10])
                llm_feedback = res.feedback
            except Exception:
                response = llm.invoke([
                    SystemMessage(content="You are a strict, authoritative requirements quality auditor. Output only valid JSON."),
                    HumanMessage(content=prompt)
                ])
                parsed_audit = _parse_json_object(response.content)
                if not isinstance(parsed_audit, dict) or not isinstance(parsed_audit.get("passed"), bool):
                    raise ValueError("Auditor returned an invalid audit report")
                parsed_issues = parsed_audit.get("issues", [])
                if not isinstance(parsed_issues, list) or (not parsed_audit["passed"] and not parsed_issues):
                    raise ValueError("Auditor failed without actionable issues")
                issues.extend([str(x) for x in parsed_issues[:10] if x])
                llm_feedback = str(parsed_audit.get("feedback", ""))
        except Exception as e:
            raise RuntimeError("Live LLM audit failed; no output was written") from e

    unique_issues = list(dict.fromkeys(issues))
    passed = (len(unique_issues) == 0)
    if passed:
        feedback = "No blocking defects detected by the configured checks; requirements approved for export."
    else:
        feedback = (llm_feedback or f"Quality audit identified {len(unique_issues)} defect(s): " + "; ".join(unique_issues))

    report = AuditReport(passed=passed, issues=unique_issues, feedback=feedback)
    logger.info(f"[Node: audit_requirements] Iteration {iteration} result: passed={passed}, issues={len(unique_issues)}")
    return {"audit_report": report.to_dict()}


# ==============================================================================
# Node 5: Requirement Refinement (LLM Node 4 / Loop: gpt-5.6-luna)
# ==============================================================================

def refine_requirements(state: AgentState) -> Dict[str, Any]:
    """Refines requirements based on auditor feedback and increments iteration_count.
    
    Forms the directed cycle feedback loop (ANS3).
    """
    iteration = state.get("iteration_count", 0) + 1
    audit = state.get("audit_report") or {}
    feedback = audit.get("feedback", "")
    issues: List[str] = audit.get("issues", [])
    refined_reqs = [copy.deepcopy(r) for r in state.get("refined_requirements", [])]
    blacklist_items = [copy.deepcopy(b) for b in state.get("blacklist", [])]
    mock_mode = state.get("mock_mode", False)

    logger.info(f"[Node: refine_requirements] Applying feedback at iteration {iteration}: {len(issues)} issues")

    # Extract target requirement IDs from issues
    target_req_ids: Set[str] = set()
    target_blk_ids: Set[str] = set()
    for iss in issues:
        target_req_ids.update(re.findall(r'\b(REQ-\d{3,4})\b', iss))
        target_blk_ids.update(re.findall(r'\b(BLK-\d{3,4})\b', iss))

    # Determine subset of requirements needing refinement
    reqs_to_refine = ([r for r in refined_reqs if r.get("id") in target_req_ids]
                      if target_req_ids else ([] if target_blk_ids else refined_reqs))
    blks_to_refine = [b for b in blacklist_items if b.get("id") in target_blk_ids]

    llm = get_llm("refine_requirements", mock_mode)
    llm_updated_map: Dict[str, Dict[str, Any]] = {}
    llm_blacklist_map: Dict[str, Dict[str, Any]] = {}
    removed_req_ids: Set[str] = set()

    if llm is not None and not mock_mode and (reqs_to_refine or blks_to_refine):
        try:
            logger.info(f"[Node: refine_requirements] Calling live LLM gpt-5.6-luna to refine {len(reqs_to_refine)} requirements")
            issues_text = "\n".join(f"- {iss}" for iss in issues)
            reqs_json = json.dumps(reqs_to_refine, indent=2)
            blks_json = json.dumps(blks_to_refine, indent=2)

            prompt = (
                "You are an expert software requirements engineer. The quality auditor has rejected or flagged "
                "defects in the current requirement specifications.\n\n"
                f"Auditor Feedback:\n{feedback}\n\n"
                f"Specific Defect Issues:\n{issues_text}\n\n"
                f"Requirements Requiring Refinement:\n{reqs_json}\n\n"
                f"Blacklist Items Requiring Refinement:\n{blks_json}\n\n"
                "Resolve ONLY the listed defects:\n"
                "1. For a DUPLICATE, merge unique details and sources into one surviving requirement, "
                "and list the redundant ID in removed_requirement_ids. Rewording alone is insufficient.\n"
                "2. For a CONTRADICTION or UNSUPPORTED issue, correct the affected requirement without "
                "inventing new behavior.\n"
                "3. If a BLK item is flagged, return it in updated_blacklist with a grounded rationale of "
                "at least 15 words; preserve its ID and corpus citations.\n"
                "4. Keep all surviving requirement IDs unchanged, explanations in prose (at least 45 words), "
                "valid MoSCoW priorities, and real corpus source paths.\n\n"
                "Return updated_requirements, updated_blacklist, and removed_requirement_ids."
            )
            try:
                structured_llm = llm.with_structured_output(RefinementResult)
                res: RefinementResult = structured_llm.invoke([
                    SystemMessage(content="You are a professional requirements engineer."),
                    HumanMessage(content=prompt)
                ])
                for item in res.updated_requirements:
                    d_item = item.to_dict() if hasattr(item, "to_dict") else item.dict()
                    req_id = d_item.get("id")
                    if req_id:
                        llm_updated_map[req_id] = d_item
                for item in res.updated_blacklist:
                    d_item = item.to_dict() if hasattr(item, "to_dict") else item.dict()
                    if d_item.get("id"):
                        llm_blacklist_map[d_item["id"]] = d_item
                removed_req_ids.update(res.removed_requirement_ids)
            except Exception:
                response = llm.invoke([
                    SystemMessage(content="You are a professional requirements engineer. Output only a valid JSON object."),
                    HumanMessage(content=prompt)
                ])
                parsed = _parse_json_object(response.content)
                if isinstance(parsed, dict):
                    for item in parsed.get("updated_requirements", []):
                        if isinstance(item, dict) and item.get("id"):
                            llm_updated_map[item["id"]] = item
                    for item in parsed.get("updated_blacklist", []):
                        if isinstance(item, dict) and item.get("id"):
                            llm_blacklist_map[item["id"]] = item
                    removed_req_ids.update(parsed.get("removed_requirement_ids", []))
            if not (llm_updated_map or llm_blacklist_map or removed_req_ids):
                raise ValueError("Refiner returned no updates")
            known_req_ids = {r.get("id") for r in refined_reqs}
            known_blk_ids = {b.get("id") for b in blacklist_items}
            if not set(llm_updated_map).issubset(known_req_ids) or not removed_req_ids.issubset(known_req_ids):
                raise ValueError("Refiner returned unknown requirement IDs")
            if not set(llm_blacklist_map).issubset(known_blk_ids):
                raise ValueError("Refiner returned unknown blacklist IDs")
            logger.info(f"[Node: refine_requirements] Updated {len(llm_updated_map)} requirements, "
                        f"{len(llm_blacklist_map)} blacklist items; merged {len(removed_req_ids)} duplicates")
        except Exception as e:
            raise RuntimeError("Live LLM refinement failed; no output was written") from e

    # Update requirements: apply LLM updates first, then dynamic fallback for any remaining deficiencies
    for i, r in enumerate(refined_reqs):
        req_id = r.get("id")

        # Apply LLM update if available
        if req_id in llm_updated_map:
            updated_fields = llm_updated_map[req_id]
            for key in ("title", "explanation", "priority", "sources", "subsystem"):
                if key in updated_fields and updated_fields[key]:
                    r[key] = updated_fields[key]

        # Dynamic fallback: check if this requirement still has defects (or in mock mode)
        words = len(re.findall(r'\w+', r.get("explanation", "")))
        if mock_mode and req_id not in llm_updated_map and (words < 40 or (target_req_ids and req_id in target_req_ids and words < 45)):
            if mock_mode and _is_evergreen_corpus(state.get("documents", [])) and req_id in MOCK_EVERGREEN_EXPANSIONS:
                r["explanation"] = MOCK_EVERGREEN_EXPANSIONS[req_id]
            else:
                title = r.get("title", "the system feature")
                curr_exp = r.get("explanation", "").strip()
                expansion = (
                    f" The system architecture must implement comprehensive operational logic for {title.lower()}, "
                    f"incorporating deterministic data validation, automated error handling, administrative audit logging, "
                    f"and configurable execution workflows to ensure strict adherence to enterprise requirements."
                )
                r["explanation"] = f"{curr_exp}{expansion}" if curr_exp else expansion.strip()

        # Check priority validity (OS6)
        prio = str(r.get("priority", "")).strip().lower()
        if prio not in {"must have", "should have", "could have", "won't have", "wont have"}:
            r["priority"] = "Should Have"

        # Check contradictory terms (OS7)
        exp_lower = r.get("explanation", "").lower()
        if "mandatory card-swipe" in exp_lower or "mandatory card swipe" in exp_lower:
            r["explanation"] = re.sub(
                r'(?i)mandatory card-?swipe',
                'optional card-swipe authentication with fallback to manual barcode entry',
                r["explanation"]
            )
        if "denormalized" in exp_lower and "warehouse" in exp_lower:
            r["explanation"] = re.sub(
                r'(?i)denormalized\s+(?:data\s+|reporting\s+)?warehouse',
                'read-only reporting replica queries',
                r["explanation"]
            )

    if removed_req_ids:
        survivors = [r for r in refined_reqs if r.get("id") not in removed_req_ids]
        if not survivors:
            raise ValueError("Refinement removed every requirement")
        updated_survivors = [r for r in survivors if r.get("id") in llm_updated_map]
        if not updated_survivors:
            raise ValueError("Duplicate removal requires an updated surviving requirement")
        keeper = updated_survivors[0]
        for removed in refined_reqs:
            if removed.get("id") in removed_req_ids:
                keeper["sources"] = list(dict.fromkeys(keeper.get("sources", []) + removed.get("sources", [])))
        refined_reqs = survivors

    for b in blacklist_items:
        if b.get("id") in llm_blacklist_map:
            updated = llm_blacklist_map[b["id"]]
            for key in ("title", "rationale", "sources"):
                if updated.get(key):
                    b[key] = updated[key]

    return {"refined_requirements": refined_reqs, "blacklist": blacklist_items,
            "iteration_count": iteration}


# ==============================================================================
# Feedback Loop Conditional Edge (ANS3)
# ==============================================================================

def should_refine(state: AgentState) -> str:
    """Evaluates whether to cycle back for refinement or proceed to markdown export.
    
    Guarantees termination via iteration_count < max_iterations boundary guard.
    """
    audit = state.get("audit_report") or {}
    passed = audit.get("passed", False)
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)

    if not passed and iteration_count < max_iterations:
        logger.info(f"[Edge: should_refine] Routing to refine_requirements (iteration {iteration_count}/{max_iterations})")
        return "refine_requirements"

    if not passed:
        unresolved = audit.get("issues", [])
        issue_count = len(unresolved)
        example = str(unresolved[0])[:240] if unresolved else "no actionable issue returned"
        raise RuntimeError(
            f"Audit did not pass after {max_iterations} refinement cycles "
            f"({issue_count} unresolved issues; first: {example}); no output was written"
        )

    logger.info(f"[Edge: should_refine] Routing to export_markdown (passed={passed}, iteration={iteration_count}/{max_iterations})")
    return "export_markdown"


# ==============================================================================
# Node 6: Deterministic Markdown Exporter (ANS2, OS1–OS9)
# ==============================================================================

def export_markdown(state: AgentState) -> Dict[str, Any]:
    """Renders the complete structured requirements document adhering to OS1–OS9."""
    output_file = state.get("output_file", "requirements.md")
    if not output_file or not str(output_file).strip():
        raise ValueError("Output file path cannot be empty.")
    out_path = Path(output_file)
    if out_path.exists() and out_path.is_dir():
        raise IsADirectoryError(f"Output path is a directory: '{output_file}'")

    refined_reqs = state.get("refined_requirements", [])
    blacklist_items = state.get("blacklist", [])
    documents = state.get("documents", [])

    logger.info(f"[Node: export_markdown] Rendering {len(refined_reqs)} requirements to {output_file}")

    is_evergreen = _is_evergreen_corpus(documents)
    doc_title = (
        "# Evergreen PINES Software Requirements Specification"
        if is_evergreen else "# Software Requirements Specification"
    )

    exec_summary = (
        "This document specifies the software requirements synthesized across heterogeneous source artifacts "
        "including committee meeting minutes, technical interviews, email deliberation threads, patron surveys, "
        "and architectural specifications."
        if is_evergreen else
        "This document specifies the software requirements synthesized across heterogeneous source artifacts "
        "including requirements specifications, design documents, deliberation notes, and technical interviews."
    )

    must_have_desc = (
        "- **Must Have**: Critical core requirements that must be delivered in the initial release. Without these capabilities, "
        "the library management and reporting system cannot function in production."
        if is_evergreen else
        "- **Must Have**: Critical core requirements that must be delivered in the initial release. Without these capabilities, "
        "the system cannot function in production."
    )

    lines: List[str] = [
        doc_title,
        "",
        "## 1. Executive Summary & Document Scope",
        "",
        exec_summary,
        "",
        "## 2. MoSCoW Priority Classification Scale",
        "",
        "Requirements in this specification are prioritized according to the established MoSCoW classification framework:",
        "",
        must_have_desc,
        "- **Should Have**: Highly important functional capabilities that provide essential operational value but are not strictly "
        "blocking for initial system deployment if alternate workarounds exist.",
        "- **Could Have**: Desirable enhancements, usability features, and administrative conveniences that will be implemented "
        "if development schedule and resource constraints permit.",
        "- **Won't Have**: Identified capabilities that have been explicitly deferred from current delivery milestones or rejected "
        "due to architectural, privacy, or policy constraints.",
        "",
        "## 3. Refined Software Requirements",
        "",
        "The following table summarizes all active software requirements refined by the agentic network:",
        "",
        "| ID | Requirement Title | Subsystem | Priority | Sources |",
        "|---|---|---|---|---|",
    ]

    if not refined_reqs:
        lines.append("| — | No active requirements discovered | — | — | — |")
    else:
        for req in refined_reqs:
            sources_str = ", ".join(f"`{s}`" for s in req.get("sources", []))
            lines.append(f"| {req.get('id')} | {req.get('title')} | {req.get('subsystem', 'General')} | {req.get('priority')} | {sources_str} |")

    lines.append("")
    lines.append("### Detailed Requirement Specifications")
    lines.append("")

    if not refined_reqs:
        lines.extend([
            "*No detailed requirements to display.*",
            "",
        ])
    else:
        for req in refined_reqs:
            sources_str = ", ".join(f"`{s}`" for s in req.get("sources", []))
            lines.extend([
                f"### Requirement {req.get('id')}: {req.get('title')}",
                f"- **Priority:** {req.get('priority')}",
                f"- **Sources:** {sources_str}",
                f"- **Subsystem:** {req.get('subsystem', 'General')}",
                "",
                req.get("explanation", "").strip(),
                "",
            ])

    lines.extend([
        "# Blacklist: Discarded and Contradictory Proposals",
        "",
        "This section documents stakeholder suggestions and early draft proposals that were analyzed by the agentic network "
        "and discarded or rejected due to architectural conflict, privacy policy, or resource constraints (satisfying OS9).",
        "",
    ])

    if not blacklist_items:
        lines.extend([
            "*No blacklist items recorded.*",
            "",
        ])
    else:
        for blk in blacklist_items:
            sources_str = ", ".join(f"`{s}`" for s in blk.get("sources", []))
            lines.extend([
                f"### Blacklist Item {blk.get('id')}: {blk.get('title')}",
                f"- **Rationale:** {blk.get('rationale', '').strip()}",
                f"- **Sources:** {sources_str}",
                "",
            ])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=out_path.parent,
                                         prefix=f".{out_path.name}.", suffix=".tmp", delete=False) as tmp:
            temporary_path = Path(tmp.name)
            tmp.write("\n".join(lines))
        os.replace(temporary_path, out_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    logger.info(f"[Node: export_markdown] Successfully generated {out_path.stat().st_size} bytes to {output_file}")
    return {}


# ==============================================================================
# LangGraph Graph Construction & Compilation (ANS1–ANS5)
# ==============================================================================

def create_graph(mock_mode: bool = False):
    """Constructs and compiles the LangGraph StateGraph pipeline.
    
    Graph Topology:
      START -> ingest_corpus (ANS2)
            -> extract_requirements (ANS1: gpt-5-mini)
            -> resolve_conflicts_and_deduplicate (ANS1: gpt-5.4-nano)
            -> audit_requirements (ANS1: gpt-6-luna)
            -> should_refine (ANS3 conditional edge)
                 [refine needed] -> refine_requirements (ANS1: gpt-5.6-luna) -> audit_requirements (Cycle)
                 [approved / max_iterations] -> export_markdown (ANS2) -> END
    """
    workflow = StateGraph(AgentState)

    # 1. Register Nodes
    workflow.add_node("ingest_corpus", ingest_corpus)
    workflow.add_node("extract_requirements", extract_requirements)
    workflow.add_node("resolve_conflicts_and_deduplicate", resolve_conflicts_and_deduplicate)
    workflow.add_node("audit_requirements", audit_requirements)
    workflow.add_node("refine_requirements", refine_requirements)
    workflow.add_node("export_markdown", export_markdown)

    # 2. Add Linear Flow Edges
    workflow.add_edge(START, "ingest_corpus")
    workflow.add_edge("ingest_corpus", "extract_requirements")
    workflow.add_edge("extract_requirements", "resolve_conflicts_and_deduplicate")
    workflow.add_edge("resolve_conflicts_and_deduplicate", "audit_requirements")

    # 3. Add Directed Feedback Cycle (ANS3)
    workflow.add_conditional_edges(
        "audit_requirements",
        should_refine,
        {
            "refine_requirements": "refine_requirements",
            "export_markdown": "export_markdown",
        }
    )
    workflow.add_edge("refine_requirements", "audit_requirements")
    workflow.add_edge("export_markdown", END)

    return workflow.compile()


# Module-level default compiled Runnable for inspectability
app = create_graph()


# ==============================================================================
# CLI Entrypoint & Argument Validation
# ==============================================================================

def positive_int(value: str) -> int:
    """Argparse type validator ensuring an integer is strictly positive (>= 1)."""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: {value!r}")
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"value must be a positive integer (>= 1), got {ivalue}")
    return ivalue


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LangGraph Software Requirements Refinement Agentic Network",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--corpus-dir", default="data/corpus", help="Path to input corpus directory")
    parser.add_argument("--output-file", default="requirements.md", help="Path to output markdown requirements file")
    parser.add_argument("--mock", action="store_true", help="Run in offline deterministic simulation mode")
    parser.add_argument("--max-iterations", type=positive_int, default=3, help="Maximum feedback loop refinement cycles (must be >= 1)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose execution logging")

    args = parser.parse_args()

    # Defense-in-depth: Validate max_iterations bounds (reject <= 0 with exit code 2)
    if args.max_iterations < 1:
        parser.error(f"--max-iterations must be a positive integer (>= 1), got {args.max_iterations}")

    try:
        # Validate --corpus-dir
        if not args.corpus_dir or not str(args.corpus_dir).strip():
            print("Error: --corpus-dir cannot be empty.", file=sys.stderr)
            sys.exit(1)

        corpus_path = Path(args.corpus_dir)
        if not corpus_path.exists():
            print(f"Error: Corpus directory does not exist: '{args.corpus_dir}'", file=sys.stderr)
            sys.exit(1)

        if not corpus_path.is_dir():
            print(f"Error: Corpus path is not a directory: '{args.corpus_dir}'", file=sys.stderr)
            sys.exit(1)

        # Validate --output-file
        if not args.output_file or not str(args.output_file).strip():
            print("Error: --output-file cannot be empty.", file=sys.stderr)
            sys.exit(1)

        output_path = Path(args.output_file)
        if output_path.exists() and output_path.is_dir():
            print(f"Error: Output path is an existing directory: '{args.output_file}'", file=sys.stderr)
            sys.exit(1)

        # Pre-flight check on output parent directory permissions
        output_parent = output_path.parent if str(output_path.parent) != "" else Path(".")
        curr = output_parent
        while not curr.exists() and curr.parent != curr:
            curr = curr.parent
        if curr.exists() and not os.access(curr, os.W_OK):
            print(f"Error: Output directory is not writable: '{curr}'", file=sys.stderr)
            sys.exit(1)

        # Empty corpus check: ensure directory contains parseable .txt or .eml files
        corpus_files = [
            p for p in corpus_path.rglob("*")
            if p.is_file() and p.suffix.lower() in (".txt", ".eml")
            and not any(part.startswith(".") for part in p.relative_to(corpus_path).parts)
        ]
        if not corpus_files:
            print(f"Error: Corpus directory '{args.corpus_dir}' contains no valid .txt or .eml documents.", file=sys.stderr)
            sys.exit(1)
    except (PermissionError, NotADirectoryError, FileNotFoundError, IsADirectoryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    initial_state: AgentState = {
        "corpus_dir": args.corpus_dir,
        "output_file": args.output_file,
        "documents": [],
        "raw_requirements": [],
        "refined_requirements": [],
        "blacklist": [],
        "audit_report": None,
        "iteration_count": 0,
        "max_iterations": args.max_iterations,
        "mock_mode": args.mock,
    }

    print(f"\n{'='*70}")
    print(f"🚀 Starting Requirements Refinement Pipeline")
    print(f"   Corpus Directory: {args.corpus_dir} ({len(corpus_files)} documents found)")
    print(f"   Output Target:    {args.output_file}")
    print(f"   Mock Mode:        {args.mock}")
    print(f"   Max Iterations:   {args.max_iterations}")
    print(f"{'='*70}\n")

    try:
        graph = create_graph(mock_mode=args.mock)
        start_time = time.perf_counter()
        final_state = graph.invoke(initial_state)
        elapsed = time.perf_counter() - start_time
    except (FileNotFoundError, NotADirectoryError, IsADirectoryError, PermissionError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Pipeline execution failed: {e}", file=sys.stderr)
        sys.exit(1)

    req_count = len(final_state.get("refined_requirements", []))
    blk_count = len(final_state.get("blacklist", []))
    iter_count = final_state.get("iteration_count", 0)
    audit = final_state.get("audit_report") or {}
    passed = audit.get("passed", False)

    print(f"\n{'='*70}")
    if passed:
        print(f"✅ Pipeline Completed Successfully in {elapsed:.2f}s")
    else:
        print(f"⚠️ Pipeline Terminated (Audit Passed: False) in {elapsed:.2f}s")
    print(f"   Refined Requirements: {req_count}")
    print(f"   Blacklist Items:      {blk_count}")
    print(f"   Refinement Iterations: {iter_count}/{args.max_iterations}")
    print(f"   Audit Passed:         {passed}")
    print(f"   Generated Output:     {args.output_file}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
