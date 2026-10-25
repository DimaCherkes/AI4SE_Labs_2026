# Evergreen PINES Software Requirements Specification

> **Validation status: draft.** This older run ended with 16 unresolved audit issues and omits the consolidated patron-characteristics source. It has not been approved by the network.

## 1. Executive Summary & Document Scope

This document specifies the software requirements synthesized across heterogeneous source artifacts including committee meeting minutes, technical interviews, email deliberation threads, patron surveys, and architectural specifications.

## 2. MoSCoW Priority Classification Scale

Requirements in this specification are prioritized according to the established MoSCoW classification framework:

- **Must Have**: Critical core requirements that must be delivered in the initial release. Without these capabilities, the library management and reporting system cannot function in production.
- **Should Have**: Highly important functional capabilities that provide essential operational value but are not strictly blocking for initial system deployment if alternate workarounds exist.
- **Could Have**: Desirable enhancements, usability features, and administrative conveniences that will be implemented if development schedule and resource constraints permit.
- **Won't Have**: Identified capabilities that have been explicitly deferred from current delivery milestones or rejected due to architectural, privacy, or policy constraints.

## 3. Refined Software Requirements

The following table summarizes all active software requirements refined by the agentic network:

| ID | Requirement Title | Subsystem | Priority | Sources |
|---|---|---|---|---|
| REQ-001 | Reproducible material volume snapshots | Material Volume | Must Have | `conversations/conv_pines014_material_volume.eml`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-002 | Governed categories and active holds | Material Volume | Must Have | `conversations/conv_pines014_material_volume.eml`, `email_report_features.eml` |
| REQ-003 | Capacity metrics and branch drilldown | Material Volume | Must Have | `conversations/conv_pines015_capacity_interface.eml` |
| REQ-004 | Deterministic shelf allocation comparisons | Material Volume | Must Have | `conversations/conv_pines016_shelf_space.eml` |
| REQ-005 | Collection use and distribution analysis | Material Volume | Must Have | `early_draft_srs_galecia.txt` |
| REQ-006 | Missing and damaged items reporting | Material Volume | Must Have | `conversations/conv_pines019_020_missing_intransit.eml` |
| REQ-007 | Deterministic transit aging reports | Material Volume | Must Have | `conversations/conv_pines019_020_missing_intransit.eml`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-008 | Transfer labels and failure notifications | Query/Queue | Should Have | `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines015_capacity_interface.eml` |
| REQ-009 | Controlled batch item transfers | Query/Queue | Must Have | `conversations/conv_pines018_item_transfer.eml` |
| REQ-010 | Governed reusable query and input sharing | Query/Queue | Must Have | `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines014_material_volume.eml`, `email_report_features.eml`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-011 | Transfer confirmation and controlled undo | Query/Queue | Must Have | `conversations/conv_pines018_item_transfer.eml`, `survey_results_2009.txt` |
| REQ-012 | Audited sanctioned transfer reversion | Query/Queue | Should Have | `conversations/conv_pines018_item_transfer.eml`, `interview_cataloging_2009-05-08.txt` |
| REQ-013 | Permissions audit trail and transfer history tracking | Security/Auth | Must Have | `conversations/conv_pines018_item_transfer.eml` |
| REQ-014 | Deterministic purge candidate identification | Weeding/Purging | Must Have | `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt` |
| REQ-015 | Approved batch status conversion | Weeding/Purging | Must Have | `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt` |
| REQ-016 | Last-copy availability classification | Weeding/Purging | Must Have | `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt` |
| REQ-017 | Controlled deletion with retained evidence | Weeding/Purging | Should Have | `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt` |
| REQ-018 | Authorized scheduled candidate workflows | Weeding/Purging | Could Have | `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-019 | Deterministic inactive patron calculation | Patron Demographics | Must Have | `conversations/conv_pines024_inactive_patrons.eml`, `email_financial_reports.eml` |
| REQ-020 | Validated inactivity period configuration | Patron Demographics | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-021 | Electronic activity source integration | Security/Auth | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-022 | Configured inactive patron grouping | Query/Queue | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-023 | Authorized patron contact disclosure | Patron Demographics | Must Have | `conversations/conv_pines024_inactive_patrons.eml`, `email_staff_login.eml` |
| REQ-024 | Inactive patron fines flagging from financial subsystem | Financial | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-025 | Privacy-aware patron exclusions | Patron Demographics | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-026 | Protected inactive patron CSV export | Query/Queue | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-027 | Shared background execution service | Query/Queue | Must Have | `conversations/conv_pines024_inactive_patrons.eml`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-028 | Measured consortium performance capacity | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-029 | Canonical observable job lifecycle | Query/Queue | Must Have | `email_report_features.eml`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-030 | Isolated asynchronous report execution | Query/Queue | Must Have | `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt` |
| REQ-031 | Timezone-aware report scheduling | Query/Queue | Must Have | `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `survey_results_2009.txt` |
| REQ-032 | Controlled Boolean query construction | Query/Queue | Must Have | `email_report_features.eml`, `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-033 | Report templates with controlled editability and sharing | Query/Queue | Should Have | `email_report_features.eml`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-034 | Predefined executive and board report templates | Query/Queue | Must Have | `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt` |
| REQ-035 | Fair report priority scheduling | Query/Queue | Must Have | `email_report_features.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt` |
| REQ-036 | Consistent null and blank serialization | Query/Queue | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-037 | Display report selection criteria used | Query/Queue | Should Have | `evergreen_reference_2009.txt` |
| REQ-038 | Canonical job progress presentation | Query/Queue | Must Have | `survey_results_2009.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt` |
| REQ-039 | WCAG-compliant interfaces and reports | Security/Auth | Must Have | `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-040 | Owned and contextual online help | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt` |
| REQ-041 | Centralized system authorization model | Security/Auth | Must Have | `early_draft_srs_galecia.txt`, `email_staff_login.eml`, `email_report_features.eml`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt` |
| REQ-042 | Report artifact and folder permissions | Security/Auth | Must Have | `email_report_features.eml`, `email_staff_login.eml`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-043 | Authorized audited state-changing actions | Security/Auth | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines021_item_purging.eml` |
| REQ-044 | Deletion and denied-action audit trail | Security/Auth | Must Have | `conversations/conv_pines022_deletions.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-045 | Read-only reporting and sanctioned ILS boundary | Security/Auth | Must Have | `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-046 | Authoritative current historical semantics | Query/Queue | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `conversations/conv_pines014_material_volume.eml` |
| REQ-047 | Query output preserves empty values | Query/Queue | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt` |
| REQ-048 | Protected administrator diagnostics | Query/Queue | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-049 | Versioned secure external exchanges | Material Volume | Should Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-050 | Bounded OPAC availability integration | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-051 | Controlled environment configuration promotion | Query/Queue | Should Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `interview_sysadmin_2009-05-10.txt` |
| REQ-052 | Template and query promotion subset | Query/Queue | Should Have | `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt` |
| REQ-053 | Reconciled financial ledger reporting | Financial | Must Have | `email_financial_reports.eml`, `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-054 | Policy-controlled financial retention | Financial | Must Have | `email_financial_reports.eml` |
| REQ-055 | Timed patron balance threshold queries | Financial | Must Have | `email_financial_reports.eml` |
| REQ-056 | Financial breakdown and balance reports | Financial | Must Have | `email_financial_reports.eml` |
| REQ-057 | Non-duplicating financial joins | Financial | Must Have | `email_financial_reports.eml` |
| REQ-058 | Comparable item value calculation | Material Volume | Must Have | `email_financial_reports.eml` |
| REQ-059 | Anonymized demographic aggregation | Patron Demographics | Must Have | `survey_results_2009.txt` |
| REQ-060 | Large-dataset execution service usage | Query/Queue | Must Have | `conversations/conv_pines024_inactive_patrons.eml`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-061 | Accessibility acceptance test coverage | Security/Auth | Must Have | `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-062 | Validated HTML5 output | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-063 | Transactional consistency for sanctioned operations | Query/Queue | Must Have | `early_draft_srs_galecia.txt` |
| REQ-064 | Controlled supported server baseline | Query/Queue | Must Have | `early_draft_srs_galecia.txt` |
| REQ-065 | Supported browser client access | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-066 | Bounded administrative impact on OPAC | Query/Queue | Must Have | `early_draft_srs_galecia.txt` |
| REQ-067 | Bounded retry and cancellation behavior | Query/Queue | Must Have | `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-068 | Distinct shelf utilization and weeding analysis | Weeding/Purging | Must Have | `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `interview_cataloging_2009-05-08.txt` |
| REQ-069 | Controlled weeding criteria workflow | Weeding/Purging | Must Have | `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |

### Detailed Requirement Specifications

### Requirement REQ-001: Reproducible material volume snapshots
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines014_material_volume.eml`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Material Volume

Material-volume reports shall follow the temporal semantics defined authoritatively by REQ-046. Each report shall record scope, cutoff timestamp, source version, snapshot identifier, capture time, and completeness status. Missing historical inputs shall be marked unavailable and excluded from inferred totals. A historical snapshot is immutable; recreating it for the same cutoff shall reference the same snapshot or explicitly report that no immutable snapshot exists.

### Requirement REQ-002: Governed categories and active holds
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines014_material_volume.eml`, `email_report_features.eml`
- **Subsystem:** Material Volume

Authorized administrators shall define, version, approve, and retire material categories, including format, genre, and local groupings, using the category-management controls described in the cited material-volume and report-feature artifacts. Each report shall store the category-version identifier used at execution. Active holds shall include open, unfulfilled holds only; cancelled, expired, fulfilled, and deleted holds shall be excluded. Role and library-scope permissions shall govern use and publication.

### Requirement REQ-003: Capacity metrics and branch drilldown
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Subsystem:** Material Volume

The capacity view shall calculate collection count as eligible physical items, available-item count as eligible items available at period end, circulation count as qualifying completed circulations during the period, occupied shelf length as measured occupied length, and utilization as occupied length divided by installed usable length. Reports shall state numerator, denominator, exclusions, period, branch scope, and source timestamp, while supporting filtering, trends, drilldown, 500 branches, and CSV export.

### Requirement REQ-004: Deterministic shelf allocation comparisons
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Subsystem:** Material Volume

Eligible circulations shall be completed checkout, renewal, or equivalent circulation events for in-scope items during the selected reporting period, excluding cancelled, test, staff, and duplicate events. Eligible items shall be in-scope physical copies with valid category assignment at the snapshot date, excluding withdrawn, duplicate, and test records. Circulation, collection, and shelf shares shall use their stated denominators; zero denominators produce not applicable and incomplete measurements are flagged.

### Requirement REQ-005: Collection use and distribution analysis
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`
- **Subsystem:** Material Volume

Collection-use recommendations shall use thresholds supplied by a versioned, administrator-approved configuration profile. The profile shall identify each metric, numerator, denominator, reporting period, minimum sample size, threshold value, comparison operator, and recommendation text. Reports shall display the profile name and version beside every recommendation, distinguish advisory results from decisions, and permit authorized users to export aggregate supporting measurements without exposing unauthorized item or patron data.

### Requirement REQ-006: Missing and damaged items reporting
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Subsystem:** Material Volume

The date-range filter shall use the condition-event date: the timestamp at which the missing or damaged condition was recorded or last changed, rather than discovery or report-update time. Timestamps shall be converted from their source time zone into the configured report time zone before inclusive range comparison. The report shall show condition type, notes, branch, event date, and counts, while allowing branch aggregation and consortium totals.

### Requirement REQ-007: Deterministic transit aging reports
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`, `interview_cataloging_2009-05-08.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Material Volume

Parameter X shall be an integer from 1 through 3650 inclusive. A transit age is the number of calendar midnights elapsed between the transit-start date and the execution date, after both timestamps are converted to the configured report time zone and truncated to local midnight. Items are included when age is at least X; a start date equal to execution date therefore has age zero and is excluded for every valid X.

### Requirement REQ-008: Transfer labels and failure notifications
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines015_capacity_interface.eml`
- **Subsystem:** Query/Queue

Responsible staff shall mean users assigned transfer-exception responsibility for the source or destination branch, or a configured consortium transfer-operations group. The delay clock begins at the confirmed transfer-batch timestamp and uses elapsed time in the configured operational time zone. The administrator-configured threshold shall be a positive whole number of hours. Notifications occur once when the threshold is exceeded and immediately for item failure, with delivery outcomes audited.

### Requirement REQ-009: Controlled batch item transfers
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Subsystem:** Query/Queue

Traceability: conversations/conv_pines018_item_transfer.eml, section “batch transfers.” Authorized users shall select query results or explicit items, review source and destination counts, and confirm a generated pull list. Processing shall occur in chunks no larger than the configured batch size. Each item update shall commit atomically; failures shall remain unchanged and appear in an exception list, while committed items shall not be silently reversed. Any sanctioned ILS write shall use the authorized workflow defined by REQ-045.

### Requirement REQ-010: Governed reusable query and input sharing
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines014_material_volume.eml`, `email_report_features.eml`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

Saved query definitions shall contain owner, immutable version, criteria, parameter values, creation and modification timestamps, and permitted scope. Owners or administrators may share a specific version with named users, groups, or authorized library scopes; consumers may execute but cannot alter it without edit permission. Reports, transfers, and pull lists shall record the exact query-version identifier used, while construction and field authorization remain governed by REQ-032.

### Requirement REQ-011: Transfer confirmation and controlled undo
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `survey_results_2009.txt`
- **Subsystem:** Query/Queue

The undo period begins when the system records successful completion of each item movement, not when the batch is submitted. It shall be configurable from 1 through 168 hours by an authorized administrator. An undo request is valid only while the item remains at the destination and has not undergone another movement or conflicting state change; otherwise that item is rejected. Partial requests produce item-level results and sanctioned compensating movements.

### Requirement REQ-012: Audited sanctioned transfer reversion
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `interview_cataloging_2009-05-08.txt`
- **Subsystem:** Query/Queue

Traceability: conversations/conv_pines018_item_transfer.eml, section “automatic reversion”; interview_cataloging_2009-05-08.txt. Reversion rules shall specify an elapsed-day threshold or named status event, identify the transfer batch, and retrieve the original location from its audit entry. The reporting system shall submit eligible changes only through the explicitly authorized ILS workflow. Moved, checked-out, or invalid-location items shall be skipped, logged with reason and retry state, and never overwritten directly.

### Requirement REQ-013: Permissions audit trail and transfer history tracking
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Subsystem:** Security/Auth

Only roles granted transfer-initiate or transfer-finalize permissions may perform those actions, with authorization evaluated at execution time. Every attempt and completed movement shall record actor, role, timestamp, item identifier, batch identifier, source and destination, before-and-after location, outcome, failure reason, and automated reversion details. History shall be immutable, searchable by item and time range, and retained sufficiently to investigate repeated transfers.

### Requirement REQ-014: Deterministic purge candidate identification
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`
- **Subsystem:** Weeding/Purging

REQ-014 is authoritative for candidate grammar and reporting. Supported fields shall declare string, enumerated, integer, decimal, date, datetime, or Boolean type; supported operators shall be equals, not-equals, less-than, less-than-or-equal, greater-than, greater-than-or-equal, and for strings contains and starts-with where configured. Literals must match field type, dates use report time zone, unknown fields and invalid comparisons fail validation, and AND, OR, NOT require explicit parentheses when mixed.

### Requirement REQ-015: Approved batch status conversion
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`
- **Subsystem:** Weeding/Purging

Traceability: conversations/conv_pines021_item_purging.eml, section “approved conversion”; interview_cataloging_2009-05-08.txt; evergreen_reference_2009.txt. Reviewers shall import or select candidates from a specific REQ-014 report, preview each proposed status change, and re-evaluate the rule before confirmation. Each approved item change shall be submitted through the sanctioned ILS workflow, not direct reporting writes, and shall record actor, timestamp, prior value, new value, report identifier, success, or failure without deleting records or bypassing approval.

### Requirement REQ-016: Last-copy availability classification
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`
- **Subsystem:** Weeding/Purging

The report shall evaluate all authorized consortium copies at one identified snapshot timestamp. Availability rules shall be versioned and classify withdrawn, missing, damaged, suppressed, and other administrator-defined states; in-transit copies shall be available only when the active rule says so. It shall count eligible copies, display excluded states and reasons, and separately identify the last available copy at branch and consortium scopes without modifying catalog data.

### Requirement REQ-017: Controlled deletion with retained evidence
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`
- **Subsystem:** Weeding/Purging

Traceability: conversations/conv_pines021_item_purging.eml and conversations/conv_pines022_deletions.eml, deletion workflow sections; interview_cataloging_2009-05-08.txt; evergreen_reference_2009.txt. Deletion requires authorization, candidate preview, and explicit confirmation, then executes only through the sanctioned ILS deletion workflow. Append-only evidence shall retain resource and parent identifiers, actor, branch, timestamp, reason, authorization, and result, with tombstone metadata queryable by authorized investigators. Denied attempts are governed by REQ-044 and shall not duplicate this evidence model.

### Requirement REQ-018: Authorized scheduled candidate workflows
- **Priority:** Could Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Weeding/Purging

Traceability: conversations/conv_pines021_item_purging.eml, scheduled purge section; interview_cataloging_2009-05-08.txt; meeting_tech_subcommittee_2009-06-30.txt. Scheduled jobs shall create REQ-014 read-only candidate reports by default, recording schedule, rule version, scope, execution time, and outcome. The scheduler shall not delete records or change statuses. If a separately approved product workflow is enabled, it must invoke the authorized ILS interface, require configured confirmation and permissions, and emit the audit records required by REQ-015 or REQ-017.

### Requirement REQ-019: Deterministic inactive patron calculation
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `email_financial_reports.eml`
- **Subsystem:** Patron Demographics

For each patron, the system shall select the latest successfully ingested qualifying event from checkout, return, renewal, hold placement or fulfillment, authenticated login, or configured digital access. Events shall be deduplicated by source identifier and converted to UTC while retaining source zone. Inactivity is true when the elapsed calendar-day value reaches the configured inclusive threshold. Missing source periods shall produce incomplete status, never a false inactive result.

### Requirement REQ-020: Validated inactivity period configuration
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Patron Demographics

X shall be a finite decimal from 0.00 through 3650.00 inclusive with no more than two fractional digits. Fractional days shall be measured as elapsed hours divided by 24 from the latest qualifying event to report execution, after conversion to UTC; a patron qualifies when elapsed time is greater than or equal to X multiplied by 24 hours. Presets 30, 90, 180, and 365 shall remain available, and invalid values shall be rejected before execution.

### Requirement REQ-021: Electronic activity source integration
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Security/Auth

Adapters shall ingest authenticated OPAC login, online hold placement, online renewal, and successful configured digital-collection access. Each event shall include source name, stable event identifier, patron identifier, event type, source timestamp, source time zone, ingestion timestamp, and status. Only successfully ingested events participate in REQ-019; unavailable adapters or source intervals shall be reported with coverage boundaries and an incomplete-data warning.

### Requirement REQ-022: Configured inactive patron grouping
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Query/Queue

Traceability: conversations/conv_pines024_inactive_patrons.eml, section “scope and grouping.” Supported scopes shall be system, consortium, library branch, county, and administrator-defined groups. Only an authorized administrator may create or modify groups; each group shall contain explicit library identifiers and an effective version. Membership shall be resolved from the patron’s current home-library relationship at snapshot time, and unauthorized users shall see only scopes granted by role.

### Requirement REQ-023: Authorized patron contact disclosure
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `email_staff_login.eml`
- **Subsystem:** Patron Demographics

The report shall select the latest non-expired address whose effective interval contains the report timestamp, using the authoritative patron-contact source and its recorded time zone. Outreach-authorized roles may view permitted fields; all others receive masked values or unavailable indicators. Access and export events shall record actor, purpose, fields, and outcome. Contact data shall be encrypted in transit and at rest and omitted from unauthorized downstream artifacts.

### Requirement REQ-024: Inactive patron fines flagging from financial subsystem
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Financial

Outstanding fines or fees shall be determined from the authoritative account-balance ledger at the report as-of timestamp. Posted, non-waived, non-reversed, non-refunded debit balances reduce by posted payments; pending, disputed, waived, and reversed amounts are excluded unless the configured financial policy explicitly includes them. The report shall show balance timestamp, included components, and a separate flag or section, with unavailable financial data marked incomplete.

### Requirement REQ-025: Privacy-aware patron exclusions
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Patron Demographics

Traceability: conversations/conv_pines024_inactive_patrons.eml, section “privacy exclusions.” The selected exclusion policy shall be evaluated before result display, caching, notification, or export. A record excluded by do-not-disturb, VIP, staff, or communication-opt-out status shall remain excluded unless an explicitly named, administrator-approved exception policy grants access for a documented purpose. The exception identifier, actor, and reason shall be audited, while excluded identities shall not appear in ordinary job metadata.

### Requirement REQ-026: Protected inactive patron CSV export
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Query/Queue

Traceability: conversations/conv_pines024_inactive_patrons.eml, section “CSV export.” Export shall accept only authorized columns and produce UTF-8 CSV with declared delimiter, header, quoting, and line-ending settings. REQ-025’s exclusion policy shall be re-evaluated against the current source state immediately before export; only its named exception mechanism may permit an excluded record. The system shall audit requester, policy, columns, row count, expiry, and secure-download access, and shall prevent unauthorized retention.

### Requirement REQ-027: Shared background execution service
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Traceability: conversations/conv_pines024_inactive_patrons.eml, execution section; evergreen_reference_2009.txt; interview_sysadmin_2009-05-10.txt; meeting_minutes/meeting_2009-07-20_minutes.txt. One persistent service shall accept scheduled and on-demand jobs and provide the canonical lifecycle in REQ-029. Cache entries shall be keyed by report definition, parameters, policy version, source snapshot, and permissions. Change events shall invalidate affected keys within five minutes; permission or policy changes shall invalidate all affected entries, and manual purge shall be immediate.

### Requirement REQ-028: Measured consortium performance capacity
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

The approved benchmark catalog shall be a controlled, versioned artifact listing representative interactive queries and standard reports, datasets, parameter values, warm or cold-cache state, concurrency, duration, percentile calculation, and exclusions. Acceptance shall use the stated 500-branch, circulation, acquisition, and concurrency workload. Administrative queries require 95th-percentile completion within five seconds, standard reports within ten minutes, and OPAC availability at least 99.9% during the defined monthly window, excluding approved maintenance.

### Requirement REQ-029: Canonical observable job lifecycle
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Traceability: email_report_features.eml, job status section; evergreen_reference_2009.txt; interview_sysadmin_2009-05-10.txt; meeting_tech_subcommittee_2009-06-30.txt; meeting_minutes/meeting_2009-07-20_minutes.txt. This requirement is authoritative for lifecycle states: queued, running, cancelling, completed, failed, and cancelled. It shall record submitter and transition timestamps, expose measurable progress, permit cancellation only before commit, and audit every transition. REQ-038 supplies progress presentation, while REQ-067 supplies retry and restart rules without redefining states.

### Requirement REQ-030: Isolated asynchronous report execution
- **Priority:** Must Have
- **Sources:** `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Subsystem:** Query/Queue

REQ-030 is authoritative for production-resource protection. Reports shall execute asynchronously in isolated workers against a reporting tier or read-only replica and shall never write ILS production data. Under the versioned REQ-028 workload, CPU, memory, database connections, and I/O shall each be measured over synchronized rolling five-minute windows against separately recorded production baselines; administrative usage must remain below 20% of every baseline, with throttling before breach.

### Requirement REQ-031: Timezone-aware report scheduling
- **Priority:** Must Have
- **Sources:** `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `survey_results_2009.txt`
- **Subsystem:** Query/Queue

Traceability: evergreen_reference_2009.txt; interview_sysadmin_2009-05-10.txt; survey_results_2009.txt. Schedules shall use IANA time zones and RFC 5545-compatible recurrence rules. For a nonexistent daylight-saving time, the scheduler shall move to the next valid local time; for a repeated time, it shall run once. A missed run shall be recorded and skipped, and an overlapping run shall be skipped while the prior instance runs. Delivery shall use TLS, authorized recipients, recorded outcomes, and cancellation support.

### Requirement REQ-032: Controlled Boolean query construction
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`, `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

The query designer shall expose only authorized fields and validated join paths, with field types and permissible operators defined by the controlled data dictionary. It shall support picklists, AND, OR, and NOT, using precedence NOT then AND then OR; mixed precedence must be made explicit with parentheses. Validation shall reject unauthorized fields, incompatible literals, ambiguous joins, and malformed expressions, then display generated criteria before a permitted user saves the definition.

### Requirement REQ-033: Report templates with controlled editability and sharing
- **Priority:** Should Have
- **Sources:** `email_report_features.eml`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

Administrators shall create, publish, version, clone, archive, and distribute report templates containing query definition, layout, permitted parameters, and output format. Each parameter and display field shall be marked fixed, administrator-editable, or staff-editable. Staff may run published templates or clone them without changing protected definitions. Sharing, folders, and execution shall use effective permissions, and every publication or revision shall record actor, timestamp, and version.

### Requirement REQ-034: Predefined executive and board report templates
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt`
- **Subsystem:** Query/Queue

The system shall supply an acceptance-catalog template set containing, at minimum, collection size and change, circulation and usage, acquisitions and expenditures, branch performance, patron activity, and financial summary reports. Each template shall define fixed query logic, reporting period, approved parameters, data-source version, required charts or tables, and export format. Administrators may publish revisions, while end users may run approved versions without constructing ad-hoc queries.

### Requirement REQ-035: Fair report priority scheduling
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Subsystem:** Query/Queue

The queue shall support Low, Normal, High, and Critical levels ordered by priority and FIFO submission time. A waiting Normal job reaching 30 minutes or being bypassed by five higher-priority job starts shall be promoted exactly once to High, and that level persists until execution begins. Promotion does not repeatedly escalate the job. Authorized priority changes require actor, old and new levels, reason, timestamp, and audit entry.

### Requirement REQ-036: Consistent null and blank serialization
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Traceability: meeting_tech_subcommittee_2009-06-30.txt; survey_results_2009.txt; meeting_minutes/meeting_2009-07-20_minutes.txt. REQ-036 is authoritative for format serialization and supersedes duplicate preservation language in REQ-047. CSV shall encode NULL as an empty field and empty string identically, with a companion schema marking nullable columns; XLSX shall use an empty cell for NULL and a zero-length string cell for empty string; HTML shall use an empty cell for both. Row and column cardinality shall remain unchanged.

### Requirement REQ-037: Display report selection criteria used
- **Priority:** Should Have
- **Sources:** `evergreen_reference_2009.txt`
- **Subsystem:** Query/Queue

Every completed, failed, previewed, or exported report shall display and retain the effective selection criteria used for execution. The criteria record shall include report or template version, saved query identifier and version when applicable, filters, date range, time zone, scope, category version, snapshot identifier, and system-applied defaults. Users shall be able to retrieve this record with the result so reruns can reproduce or explain the output.

### Requirement REQ-038: Canonical job progress presentation
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`
- **Subsystem:** Query/Queue

Traceability: survey_results_2009.txt; evergreen_reference_2009.txt; interview_sysadmin_2009-05-10.txt. For countable jobs, the interface shall show completed units, total units, percentage, start time, elapsed time, and throughput-based estimate; for non-countable jobs it shall show phase and elapsed time without inventing a percentage. Status shall refresh at least every 30 seconds. Historical durations shall be restricted by report permissions, and lifecycle, retry, and cancellation semantics shall come only from REQ-029 and REQ-067.

### Requirement REQ-039: WCAG-compliant interfaces and reports
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Security/Auth

Traceability: early_draft_srs_galecia.txt; interview_sysadmin_2009-05-10.txt; meeting_minutes/meeting_2009-07-20_minutes.txt; meeting_tech_subcommittee_2009-06-30.txt. REQ-039 is authoritative for WCAG 2.1 Level AA conformance across administrative screens and generated HTML reports; REQ-061 adds only its test matrix. Release testing shall include keyboard-only operation, focus order, semantic structure, labels, contrast, alternatives, tables, representative screen readers, and supported browsers. Critical navigation or interpretation failures shall block acceptance.

### Requirement REQ-040: Owned and contextual online help
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Subsystem:** Query/Queue

Each supported report, parameter, workflow, and error state shall map to a stable context identifier and versioned HTML help topic. The controlled help catalog shall assign owner, reviewer, publication date, and release version, and require hierarchical navigation, search, cross-links, and contextual access. Release validation shall verify every referenced identifier resolves, every required topic is published, and no broken links remain in supported interfaces or exports.

### Requirement REQ-041: Centralized system authorization model
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `email_staff_login.eml`, `email_report_features.eml`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Subsystem:** Security/Auth

A centralized role- and group-based authorization service shall evaluate authentication, report creation, execution, scheduling, export, administration, patron-data access, deletion, and configuration at every API and interface boundary. Decisions shall deny by default and record actor, effective roles, resource, action, policy version, and result. Role or group changes shall be visible on the next authorization check, without per-user permission edits, and authorization failures shall not disclose protected data.

### Requirement REQ-042: Report artifact and folder permissions
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`, `email_staff_login.eml`, `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Security/Auth

Owners or administrators shall assign view, edit, clone, execute, schedule, export, and folder-management permissions to named users or groups for each report artifact. Shared folders shall inherit permissions by default; overrides are permitted only where the authorization model explicitly supports them. The system shall display effective permissions to authorized administrators and re-evaluate artifact access immediately after role or membership changes, recording denied attempts for audit.

### Requirement REQ-043: Authorized audited state-changing actions
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines021_item_purging.eml`
- **Subsystem:** Security/Auth

Traceability: meeting_tech_subcommittee_2009-06-30.txt; meeting_minutes/meeting_2009-07-20_minutes.txt; conversations/conv_pines018_item_transfer.eml; conversations/conv_pines021_item_purging.eml. Any record-changing operation shall require role authorization, preview where applicable, explicit confirmation, and invocation of the sanctioned ILS workflow described by REQ-045. The reporting system shall not write ILS data directly. Submission, cancellation request, completion, failure, actor, and affected-item counts shall be audited, while operation-specific evidence remains governed by REQ-015 and REQ-017.

### Requirement REQ-044: Deletion and denied-action audit trail
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines022_deletions.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Security/Auth

REQ-044 is authoritative for successful and denied deletion attempts. Each append-only event shall record resource type and stable identifier, actor, branch, synchronized timestamp, requested action, authorization result, reason, parent relationship, transaction outcome, and policy version. Audit records shall be retained for the duration specified by the controlled records-retention policy, or longer where a legal hold applies, and authorized investigators shall query them without unrelated patron fields.

### Requirement REQ-045: Read-only reporting and sanctioned ILS boundary
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Security/Auth

Traceability: meeting_tech_subcommittee_2009-06-30.txt, section “read-only ILS integration.” Reporting connections shall use credentials lacking write, schema-change, and procedure-execution privileges, and application validation shall reject write statements. Record-changing transfers, status conversions, reversions, and deletions are permitted only through a separately deployed, explicitly authorized ILS workflow interface with its own permissions, confirmation, transaction, and audit controls. Reporting services may submit requests but shall not execute direct mutations; rejected attempts shall be audited.

### Requirement REQ-046: Authoritative current historical semantics
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `conversations/conv_pines014_material_volume.eml`
- **Subsystem:** Query/Queue

REQ-046 is authoritative for temporal reporting. Current reports read the latest authoritative state at execution; historical reports read an immutable snapshot identified by scope, cutoff, source version, capture time, and completeness. Corrections or deletions made after the cutoff are not retroactively inserted into that snapshot. Recreating the same cutoff shall return the same immutable snapshot and result; if none exists, the system shall report unavailable rather than silently substitute later data.

### Requirement REQ-047: Query output preserves empty values
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Subsystem:** Query/Queue

Traceability: meeting_tech_subcommittee_2009-06-30.txt; survey_results_2009.txt. Query results shall retain every source row and column, including values that are NULL or empty strings, and shall never omit rows or collapse columns during rendering, filtering, pagination, or export. Format-specific representation is defined exclusively by REQ-036, including its companion nullable-column metadata. Consumers shall therefore receive deterministic cardinality and explicit handling instructions without duplicate serialization rules.

### Requirement REQ-048: Protected administrator diagnostics
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Users shall receive only a non-sensitive failure message containing job identifier, error category, and recovery guidance. Authorized administrators may view correlated diagnostics containing query fragment, table or field, execution phase, and database code, with patron values, credentials, connection strings, and unrestricted SQL redacted. Diagnostics shall be encrypted, access-controlled, retained for the duration specified by the controlled retention policy, and audited whenever viewed, downloaded, or exported.

### Requirement REQ-049: Versioned secure external exchanges
- **Priority:** Should Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Material Volume

The controlled interoperability profile registry shall identify the approved MARC21 revision and UN/EDIFACT message-directory release for every partner; profiles lacking those versions are invalid. Compatibility shall be checked against the registry before activation and during exchange validation. Each profile shall define direction, schema, encoding, idempotency key, acknowledgement, timeout, retry limit, quarantine behavior, and no-partial-import handling. HTTPS requires TLS 1.2 or later and SFTP requires SSH public-key authentication.

### Requirement REQ-050: Bounded OPAC availability integration
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

Traceability: early_draft_srs_galecia.txt; meeting_tech_subcommittee_2009-06-30.txt. The management component is the configured ILS availability interface, and latency is measured from source event availability to successful reporting-tier receipt. Under normal operation, synchronization shall complete within five minutes. After failure, the system shall retain the last successful snapshot, mark it stale with timestamp, retry after 1, 2, 4, 8, and 16 minutes, then cap retries at 30-minute intervals; stale data shall never be labeled current or block OPAC transactions.

### Requirement REQ-051: Controlled environment configuration promotion
- **Priority:** Should Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `interview_sysadmin_2009-05-10.txt`
- **Subsystem:** Query/Queue

Traceability: early_draft_srs_galecia.txt; meeting_minutes/meeting_2009-07-20_minutes.txt; meeting_tech_subcommittee_2009-06-30.txt; interview_sysadmin_2009-05-10.txt. Promotion shall be the single authoritative process for templates, saved queries, schedules, permissions, categories, and reference data; REQ-052 is its template/query subset. Versioned packages shall validate dependencies and conflicts, require approval before production import, preserve identifiers when safe, support rollback, and exclude unmasked patron or financial data from lower environments under the approved data-handling procedure.

### Requirement REQ-052: Template and query promotion subset
- **Priority:** Should Have
- **Sources:** `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Subsystem:** Query/Queue

Traceability: evergreen_reference_2009.txt; meeting_tech_subcommittee_2009-06-30.txt; survey_results_2009.txt; meeting_minutes/meeting_2009-07-20_minutes.txt; meeting_minutes/meeting_2009-03-15_minutes.txt. This requirement is limited to the template and saved-query objects covered by REQ-051. Packages shall preserve structure, filters, parameter definitions, schedule metadata, and applicable permissions, while dependency validation, approval, conflict handling, rollback, identifiers, and environment data protections shall follow REQ-051 rather than being reimplemented here.

### Requirement REQ-053: Reconciled financial ledger reporting
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`, `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Financial

Financial reports shall preserve immutable ledger events for charges, payments, waivers, refunds, reversals, corrections, and acquisitions, including event type, amount, currency, timestamp, source, actor, and branch. For each period, the system shall compare event totals with source-system control totals, classify differences by source and type, and expose discrepancies rather than adjust silently. Exports shall retain original events and linked corrections for the applicable accounting-policy period.

### Requirement REQ-054: Policy-controlled financial retention
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`
- **Subsystem:** Financial

The system shall implement retention rules approved by the applicable accounting and audit policy, including configurable retention duration by record type. Legal holds shall suspend disposal, while statutory deletion obligations shall be escalated for documented policy resolution rather than overridden silently. Retention execution shall produce an auditable report of retained, held, archived, and deleted records, and shall preserve ledger evidence required for reconciliation.

### Requirement REQ-055: Timed patron balance threshold queries
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`
- **Subsystem:** Financial

Balance queries shall specify currency, effective-as-of timestamp, home-library scope, and threshold comparison. The calculated balance shall identify included pending, posted, waived, refunded, and disputed amounts according to the configured financial policy and shall show each component. Threshold evaluation shall be inclusive or exclusive as selected, and only authorized staff may view patron-level results or export them.

### Requirement REQ-056: Financial breakdown and balance reports
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`
- **Subsystem:** Financial

Financial reports shall show balances and charge or payment totals by patron, branch, period, charge type, waiver status, and payment method using the same currency and as-of rules as REQ-055. Each report shall distinguish pending, posted, waived, refunded, reversed, and disputed amounts, support last-month, year-to-date, and rolling-period filters, and restrict patron-level output and export through authorization controls.

### Requirement REQ-057: Non-duplicating financial joins
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`
- **Subsystem:** Financial

Financial reports shall join patron, account, transaction, item, and bibliographic records through documented stable keys and declared cardinality. One-to-many relationships shall be aggregated at the intended grain before joining to another one-to-many relation, preventing duplicated charges or purchase values. Each report shall display its grain, join keys, and reconciliation totals, and validation shall compare aggregated results with source control totals.

### Requirement REQ-058: Comparable item value calculation
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`
- **Subsystem:** Material Volume

Item-value reports shall state currency and whether values represent historical purchase cost or an approved current valuation. Missing, zero, and invalid purchase prices shall be counted and reported separately rather than treated as zero without disclosure. Totals shall aggregate only the selected item grain, apply status, format, collection, location, and call-number filters deterministically, and expose included and excluded counts.

### Requirement REQ-059: Anonymized demographic aggregation
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`
- **Subsystem:** Patron Demographics

Demographic reports shall remove direct identifiers before aggregation and permit only approved geography and age-band dimensions. Cells below the configured minimum count of five shall be suppressed, combined, or rounded; complementary-cell analysis shall prevent reconstruction by subtraction across totals or overlapping views. Exports shall contain aggregate values only. A privacy administrator may approve a lower threshold only through a versioned exception with justification, expiry, scope, and audit record.

### Requirement REQ-060: Large-dataset execution service usage
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Traceability: conversations/conv_pines024_inactive_patrons.eml; evergreen_reference_2009.txt; interview_sysadmin_2009-05-10.txt; meeting_minutes/meeting_2009-07-20_minutes.txt. Large reports and queries shall use the shared service defined by REQ-027 and canonical lifecycle defined by REQ-029; this requirement does not create a second queue, cache, status model, or notification mechanism. A submission shall be on-demand or scheduled, execute asynchronously, expose its job identifier, and return control to interactive administration immediately.

### Requirement REQ-061: Accessibility acceptance test coverage
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Security/Auth

Traceability: early_draft_srs_galecia.txt; interview_sysadmin_2009-05-10.txt; meeting_minutes/meeting_2009-07-20_minutes.txt. REQ-061 is the acceptance-test subset of REQ-039, not an additional accessibility rule. Testing shall cover supported browsers and desktop operating systems, keyboard-only workflows, focus order, screen-reader navigation, generated HTML tables, export rendering, labels, contrast, and semantic structure. Each failure shall identify component, criterion, severity, and reproduction steps; critical task-blocking defects shall prevent acceptance.

### Requirement REQ-062: Validated HTML5 output
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Web pages, help topics, and HTML report exports shall declare UTF-8 and conform to the HTML Living Standard within the supported feature scope. Automated validation shall check document structure, nesting, applicable unique identifiers, encoding, and absence of validation errors against representative static pages and generated reports. The build shall retain validation results and fail release acceptance on errors, while WCAG conformance remains separately governed by REQ-039 and REQ-061.

### Requirement REQ-063: Transactional consistency for sanctioned operations
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`
- **Subsystem:** Query/Queue

Traceability: early_draft_srs_galecia.txt, persistence architecture section. The persistence layer shall provide ACID behavior for reporting metadata, requests, permissions, ledger events, and audit records, while ILS record mutations occur only in the sanctioned interface defined by REQ-045. A committed request shall have required audit metadata; a failed request shall not claim success or leave partial reporting state. Idempotency keys, unique identifiers, referential integrity, and repeatable snapshot reads shall be enforced by the approved relational architecture.

### Requirement REQ-064: Controlled supported server baseline
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`
- **Subsystem:** Query/Queue

Traceability: early_draft_srs_galecia.txt, platform support section. The approved release compatibility matrix shall be a controlled acceptance artifact, versioned and approved by the product owner before release. For this baseline it shall list Linux distributions with supported major versions Ubuntu 22.04 LTS and RHEL 9, and Solaris 11.4, plus runtime, drivers, service managers, and monitoring interfaces. Installation, health checks, representative reporting, and read-only integration tests shall pass on every listed platform.

### Requirement REQ-065: Supported browser client access
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Traceability: early_draft_srs_galecia.txt; meeting_minutes/meeting_2009-07-20_minutes.txt. The supported desktop scope is Windows 11 and macOS 14 or later minor releases approved in the compatibility matrix. Browser support means the latest two vendor-supported major versions available at release for Chrome, Edge, Firefox, and Safari, recorded by version and test date in that matrix. Every supported combination shall provide equivalent authentication, authorization, results, exports, scheduling, and REQ-039 accessibility behavior.

### Requirement REQ-066: Bounded administrative impact on OPAC
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`
- **Subsystem:** Query/Queue

REQ-066 is limited to acceptance testing of the OPAC protection outcome and does not redefine the resource limit in REQ-030. Using the same controlled REQ-028 workload, baseline, and synchronized five-minute rolling windows, load tests shall demonstrate that OPAC service-level objectives remain satisfied while REQ-030 limits hold. Tests shall include sustained and peak concurrency, record throttling or pause actions, and retain metrics proving no production breach.

### Requirement REQ-067: Bounded retry and cancellation behavior
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

Each job may receive at most three automatic retries after its initial attempt; the initial attempt is not counted as a retry. Retry delays shall be 30 seconds after retry one, two minutes after retry two, and ten minutes after retry three, unless a controlled policy changes the schedule. Cancellation shall prevent queued and future retries and be checked at submission, queue, worker, and commit checkpoints. Linked attempt identifiers and idempotency keys prevent duplicate committed work.

### Requirement REQ-068: Distinct shelf utilization and weeding analysis
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `interview_cataloging_2009-05-08.txt`
- **Subsystem:** Weeding/Purging

The shelf-utilization report shall calculate occupied shelf length divided by installed usable shelf length for each branch and category, using measurements from one identified date and source. It shall show numerator, denominator, occupancy percentage, circulation context, exclusions, and incomplete measurement status. It shall not determine purge eligibility or change item state. Candidate identification, Boolean criteria, duration rules, approval, and conversion remain exclusively delegated to REQ-014 and REQ-015.

### Requirement REQ-069: Controlled weeding criteria workflow
- **Priority:** Must Have
- **Sources:** `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Weeding/Purging

REQ-069 is a bounded extension of REQ-014 and shall not redefine its grammar, operators, field typing, or candidate-report format. It adds status, status-duration days, last-circulation date, circulation count, and location predicates using REQ-014 validation; dates use report time zone and missing values never match. Candidate creation is read-only. Batch changes require importing candidates, item-by-item revalidation, preview, confirmation, and invocation of REQ-015; bypass is prohibited.

# Blacklist: Discarded and Contradictory Proposals

This section documents stakeholder suggestions and early draft proposals that were analyzed by the agentic network and discarded or rejected due to architectural conflict, privacy policy, or resource constraints (satisfying OS9).

### Blacklist Item BLK-001: Mandatory magnetic card-swipe login as the only authentication
- **Rationale:** A requirement mandating magnetic card-swipe as compulsory and bypassing individual authentication would conflict with role-based authentication integrity and could undermine auditability and authorization. No such mandatory-bypass requirement is needed because optional card-swipe support with proper identity mapping is already covered by other proposals.
- **Sources:** `email_staff_login.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`

### Blacklist Item BLK-002: Unanonymized patron demographic reporting at individual level
- **Rationale:** Proposals requiring demographic statistics to be reported without anonymization would violate privacy expectations and compliance needs. Existing requirements already define anonymized demographic statistics for aggregated reporting, making individual-level exposure unnecessary and disallowed.
- **Sources:** `survey_results_2009.txt`, `early_draft_srs_galecia.txt`

### Blacklist Item BLK-003: Denormalized reporting warehouse required as a hard constraint
- **Rationale:** Any explicit requirement to use a denormalized reporting warehouse as mandatory storage would be an architectural constraint not supported by the rest of the text. The system only needs to provide correct historical snapshot behavior; implementation details should remain flexible to avoid conflicting design assumptions.
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `interview_sysadmin_2009-05-10.txt`
