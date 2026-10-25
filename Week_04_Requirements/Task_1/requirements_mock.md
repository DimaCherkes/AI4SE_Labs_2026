# Evergreen PINES Software Requirements Specification

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
| REQ-001 | Material Volume Calculation and Linear Shelf Space Sizing | Material Volume & Shelf Space | Must Have | `conversations/conv_pines014_material_volume.eml`, `conversations/conv_pines016_shelf_space.eml`, `early_draft_srs_galecia.txt` |
| REQ-002 | Interactive Branch Shelf Capacity and Threshold Utilization Warnings | Material Volume & Shelf Space | Should Have | `conversations/conv_pines015_capacity_interface.eml`, `conversations/conv_pines016_shelf_space.eml` |
| REQ-003 | Inter-Branch Item Transfer Manifests and In-Transit Tracking | Weeding & Purging | Must Have | `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines019_020_missing_intransit.eml` |
| REQ-004 | Item Deletion Status Distinctions and Catalog Purging Safeguards | Weeding & Purging | Must Have | `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml` |
| REQ-005 | Multi-Criteria Weeding Candidate Identification and Soft-Deletion | Weeding & Purging | Should Have | `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt` |
| REQ-006 | Patron Inactive Status Detection and Data Retention Lifecycle | Patron Demographics & Inactive | Should Have | `conversations/conv_pines024_inactive_patrons.eml`, `evergreen_reference_2009.txt` |
| REQ-007 | Patron Demographic and Geographic Distribution Analytics | Patron Demographics & Inactive | Could Have | `conversations/conv_pines023_patron_characteristics.eml`, `survey_results_2009.txt` |
| REQ-008 | Granular Staff User Authentication and Role-Based Permissions | Security & Authentication | Must Have | `email_staff_login.eml`, `evergreen_reference_2009.txt` |
| REQ-009 | Financial Fine Reconciliation and Ledger Export | Financial Reporting | Must Have | `email_financial_reports.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-010 | Standardized and Ad-Hoc Report Template Designer | Query & Queue Management | Must Have | `email_report_features.eml`, `interview_cataloging_2009-05-08.txt` |
| REQ-011 | Automated Asynchronous Report Scheduling and Email Delivery | Query & Queue Management | Should Have | `email_report_features.eml`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-012 | Background Report Queue Execution and Resource Throttling | Query & Queue Management | Must Have | `interview_sysadmin_2009-05-10.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-013 | Query Optimization and PostgreSQL Database Indexing Safeguards | Query & Queue Management | Must Have | `interview_sysadmin_2009-05-10.txt`, `evergreen_reference_2009.txt` |
| REQ-014 | Multi-Format Data Export and Encoding Standards | Query & Queue Management | Should Have | `interview_cataloging_2009-05-08.txt`, `email_report_features.eml` |
| REQ-015 | Section 508 Accessibility and Web Standards Compliance | Security & Authentication | Must Have | `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-016 | Administrative Configuration and Audit Logging Trail | Security & Authentication | Must Have | `email_staff_login.eml`, `interview_sysadmin_2009-05-10.txt` |

### Detailed Requirement Specifications

### Requirement REQ-001: Material Volume Calculation and Linear Shelf Space Sizing
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines014_material_volume.eml`, `conversations/conv_pines016_shelf_space.eml`, `early_draft_srs_galecia.txt`
- **Subsystem:** Material Volume & Shelf Space

The Evergreen ILS reporting module must calculate accurate material volumes across all physical shelving locations by converting item counts into linear shelf inches based on standardized classification call number averages. The system shall compute total linear shelf space consumption across call number ranges, branch collections, and circulating item statuses using calibrated formulaic spine thickness factors. This calculation provides branch managers with precise physical inventory footprint metrics for collection management and facility expansion planning.

### Requirement REQ-002: Interactive Branch Shelf Capacity and Threshold Utilization Warnings
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`, `conversations/conv_pines016_shelf_space.eml`
- **Subsystem:** Material Volume & Shelf Space

The system shall deliver dynamic reporting views comparing total shelving linear capacity against measured collection volumes for every branch library facility. When material volumes exceed parameterized percentage thresholds (e.g., 85% maximum capacity), the interface must trigger visual warning indicators and automated alert notifications to designated library administrators, preventing physical space overfilling and supporting proactive weeding initiatives.

### Requirement REQ-003: Inter-Branch Item Transfer Manifests and In-Transit Tracking
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`, `conversations/conv_pines019_020_missing_intransit.eml`
- **Subsystem:** Weeding & Purging

The reporting interface must track physical items moving between library branches, generating formal transfer packing slips and transit verification reports. Discrepancies between transit initiation and receipt check-in must be flagged as in-transit missing items after a configurable holding window of 14 days, preventing inventory loss during inter-library loan logistics.

### Requirement REQ-004: Item Deletion Status Distinctions and Catalog Purging Safeguards
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml`
- **Subsystem:** Weeding & Purging

The system shall enforce rigorous structural distinctions between deleted items and purged items within the reporting database schema. Soft-deleted records must remain queryable in historical statistical summaries and circulating metrics for a minimum of 24 months before irreversible permanent purge operations can be authorized by regional database administrators.

### Requirement REQ-005: Multi-Criteria Weeding Candidate Identification and Soft-Deletion
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Subsystem:** Weeding & Purging

The reporting tool shall generate multi-criteria candidate weeding lists identifying physical items with zero circulations over the preceding three years, multiple damaged condition flags, or superseded edition markers. All candidate records marked for removal must enter a two-stage soft-deletion state allowing physical shelf inspection and administrative review prior to permanent record purge execution, ensuring comprehensive preservation of historical holdings.

### Requirement REQ-006: Patron Inactive Status Detection and Data Retention Lifecycle
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`, `evergreen_reference_2009.txt`
- **Subsystem:** Patron Demographics & Inactive

The reporting module shall execute scheduled batch evaluations to flag patron accounts with zero circulation, payment, or digital authentication activity over an administrator-defined inactivity threshold (e.g., 36 months). Inactive accounts must be flagged for retention review or anonymized archival in strict compliance with state public record management mandates and patron privacy regulations.

### Requirement REQ-007: Patron Demographic and Geographic Distribution Analytics
- **Priority:** Could Have
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`, `survey_results_2009.txt`
- **Subsystem:** Patron Demographics & Inactive

The reporting subsystem shall generate aggregated demographic and postal code distribution profiles correlating patron registration density with circulation intensity and facility access patterns. To safeguard individual privacy, all geospatial reports must enforce cell suppression algorithms that mask demographic groupings representing fewer than five individuals.

### Requirement REQ-008: Granular Staff User Authentication and Role-Based Permissions
- **Priority:** Must Have
- **Sources:** `email_staff_login.eml`, `evergreen_reference_2009.txt`
- **Subsystem:** Security & Authentication

The administrative reporting module shall restrict report definition, template authoring, and query execution capabilities through an explicit role-based access control matrix. Individual staff user accounts must be authenticated against verified credentials and assigned least-privilege reporting permissions corresponding to their institutional organizational tier.

### Requirement REQ-009: Financial Fine Reconciliation and Ledger Export
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Financial Reporting

The system shall deliver comprehensive daily and monthly financial reconciliation ledgers tracking patron fine assessments, cash and card fee payments, fee forgiveness exemptions, and outstanding billing balances. All financial summaries must cross-reference terminal operator IDs and export structured reconciliation files formatted for standard municipal municipal accounting software.

### Requirement REQ-010: Standardized and Ad-Hoc Report Template Designer
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`, `interview_cataloging_2009-05-08.txt`
- **Subsystem:** Query & Queue Management

The reporting tool shall provide both a repository of standardized pre-built administrative reports and an intuitive wizard interface for constructing ad-hoc report templates. Authorized staff members must be able to select data sources, configure filter expressions, designate grouping hierarchies, and save customized template definitions for recurring departmental use.

### Requirement REQ-011: Automated Asynchronous Report Scheduling and Email Delivery
- **Priority:** Should Have
- **Sources:** `email_report_features.eml`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query & Queue Management

The system shall allow staff to schedule complex, recurring report generation jobs during off-peak processing hours (e.g., nightly or weekly). Upon task completion, the scheduling daemon must generate output files in the requested format and automatically distribute them via authenticated SMTP to designated stakeholder mailing distribution lists.

### Requirement REQ-012: Background Report Queue Execution and Resource Throttling
- **Priority:** Must Have
- **Sources:** `interview_sysadmin_2009-05-10.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query & Queue Management

All reporting queries exceeding configured runtime thresholds must execute asynchronously within a background job queue rather than in synchronous web client sessions. The queue manager shall enforce concurrency limits, thread pooling, and CPU/memory quotas to protect production transactional circulation performance from intensive analytical database queries.

### Requirement REQ-013: Query Optimization and PostgreSQL Database Indexing Safeguards
- **Priority:** Must Have
- **Sources:** `interview_sysadmin_2009-05-10.txt`, `evergreen_reference_2009.txt`
- **Subsystem:** Query & Queue Management

The reporting engine shall enforce database indexing rules and query structure validation against the underlying PostgreSQL relational engine. Ad-hoc report templates that would trigger unindexed sequential table scans on core circulation transaction tables must be intercepted and rejected with constructive optimization guidance for the author.

### Requirement REQ-014: Multi-Format Data Export and Encoding Standards
- **Priority:** Should Have
- **Sources:** `interview_cataloging_2009-05-08.txt`, `email_report_features.eml`
- **Subsystem:** Query & Queue Management

All generated tabular and summary reports must support seamless data export into industry-standard digital formats, including UTF-8 encoded Comma-Separated Values (CSV), Microsoft Excel OpenXML (XLSX), and Portable Document Format (PDF). Exported files must strictly preserve special diacritical characters, MARC 21 cataloging encodings, and numerical precision.

### Requirement REQ-015: Section 508 Accessibility and Web Standards Compliance
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Security & Authentication

All web-based reporting interfaces, parameter selection forms, and generated HTML report outputs must comply fully with Federal Section 508 accessibility guidelines and W3C WCAG 2.0 Level AA standards. Interfaces must provide full keyboard navigation, high-contrast visual display options, and semantic labeling compatible with standard screen readers.

### Requirement REQ-016: Administrative Configuration and Audit Logging Trail
- **Priority:** Must Have
- **Sources:** `email_staff_login.eml`, `interview_sysadmin_2009-05-10.txt`
- **Subsystem:** Security & Authentication

The reporting subsystem shall maintain an immutable administrative audit log capturing all system configuration modifications, template deletions, scheduled execution failures, and staff access events. Audit logs must record ISO 8601 timestamps, authenticated user identifiers, source IP addresses, and detailed modification deltas to satisfy state regulatory oversight.

# Blacklist: Discarded and Contradictory Proposals

This section documents stakeholder suggestions and early draft proposals that were analyzed by the agentic network and discarded or rejected due to architectural conflict, privacy policy, or resource constraints (satisfying OS9).

### Blacklist Item BLK-001: Mandatory Magnetic Card-Swipe for Patron Identification
- **Rationale:** Stakeholders and privacy advocates rejected mandatory card-swipe identification due to severe privacy civil liberties concerns, unnecessary hardware procurement costs, and lack of support for patrons lacking physical magnetic cards. The system instead supports optional barcode scanning and manual patron lookup.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`, `survey_results_2009.txt`

### Blacklist Item BLK-002: Real-Time Denormalized Global Reporting Warehouse
- **Rationale:** Systems administration and database engineering rejected proposals for a separate real-time denormalized data warehouse. The maintenance overhead, replication latency risks, and PostgreSQL hardware resource limitations made maintaining dual schema synchronization unsustainable. The architecture instead leverages dedicated read-only database replicas.
- **Sources:** `interview_sysadmin_2009-05-10.txt`, `meeting_tech_subcommittee_2009-06-30.txt`

### Blacklist Item BLK-003: Direct Unchecked Batch Purging of Historical Circulation Records
- **Rationale:** Proposals to allow immediate, hard-delete batch purging of circulation history without multi-stage soft-deletion and administrative approval were rejected. Direct purging presents unacceptable risks of permanent statistical data loss and violates public library accountability and audit retention policies.
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt`

### Blacklist Item BLK-004: Unrestricted Ad-Hoc Query Access to Patron PII and Financial Tables
- **Rationale:** Unrestricted ad-hoc SQL query execution against tables containing patron personally identifiable information (PII) or unmasked financial transactions was strictly rejected by committee consensus. Permitting direct access violates patron confidentiality policies and municipal financial audit controls. All reporting access must occur through governed, parameterized views.
- **Sources:** `email_staff_login.eml`, `email_financial_reports.eml`, `survey_results_2009.txt`
