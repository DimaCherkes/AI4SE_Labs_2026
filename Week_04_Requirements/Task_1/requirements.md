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
| REQ-001 | Material Volume Report at Point in Time | Material Volume | Must Have | `conversations/conv_pines014_material_volume.eml` |
| REQ-002 | System Capacity Overview Dashboard | Material Volume | Must Have | `conversations/conv_pines015_capacity_interface.eml` |
| REQ-003 | Shelf Space Versus Usage Comparative Reporting | Material Volume | Must Have | `conversations/conv_pines016_shelf_space.eml` |
| REQ-004 | Batch Item Transfer Utility With Preview | Query/Queue | Must Have | `conversations/conv_pines018_item_transfer.eml` |
| REQ-005 | Transfer Authorization, Audit Trail, and History | Security/Auth | Must Have | `conversations/conv_pines018_item_transfer.eml` |
| REQ-006 | Missing and Damaged Items Reporting | Material Volume | Must Have | `conversations/conv_pines019_020_missing_intransit.eml` |
| REQ-007 | In-Transit Items Aging With Merged View | Material Volume | Must Have | `conversations/conv_pines019_020_missing_intransit.eml` |
| REQ-008 | Item Purging Candidate Identification Report | Weeding/Purging | Must Have | `conversations/conv_pines021_item_purging.eml` |
| REQ-009 | Candidate Reporting and Batch Item Status Conversion | Weeding/Purging | Must Have | `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `conversations/conv_pines022_deletions.eml`, `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt` |
| REQ-010 | Last Copy Identification Report for Deletion Safety | Weeding/Purging | Must Have | `conversations/conv_pines021_item_purging.eml` |
| REQ-011 | Purge and Delete Confirmation Controls With Audit Trail | Weeding/Purging | Must Have | `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml` |
| REQ-012 | Queryable Deletion Logging and Accountability Reports | Security/Auth | Must Have | `conversations/conv_pines022_deletions.eml`, `survey_results_2009.txt` |
| REQ-013 | Patron Demographic Querying and Grouped Aggregations | Patron Demographics | Must Have | `conversations/conv_pines023_patron_characteristics.eml` |
| REQ-014 | In-Active Patrons Report With Configurable Inactivity | Patron Demographics | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-015 | Inactive Patrons Reporting Scope and Data Outputs | Patron Demographics | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-016 | CSV Export for Inactive Patrons Report | Query/Queue | Must Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-017 | Background Processing and Caching for Inactive Patrons Report | Query/Queue | Should Have | `conversations/conv_pines024_inactive_patrons.eml` |
| REQ-018 | Management Processes Reporting Capabilities Across Enterprise | Query/Queue | Must Have | `early_draft_srs_galecia.txt` |
| REQ-019 | Centralized Multi-Location Management Services | Query/Queue | Must Have | `early_draft_srs_galecia.txt` |
| REQ-020 | Report and Search Processing During Open Hours | Query/Queue | Must Have | `early_draft_srs_galecia.txt` |
| REQ-021 | Web Browser and Windows Client Access for Management Tools | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-022 | Browser Compatibility for Web Interface | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-023 | Assistive Technology Support for Management Interfaces | Patron Demographics | Must Have | `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-024 | Relational Database Backend for Management Processes | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-025 | Standards-Compliant HTML Output for Web Components | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-026 | Development and Training Environment With Migratable Configurations | Security/Auth | Should Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-027 | Role and Group Based Access Control for Management Functions | Security/Auth | Must Have | `early_draft_srs_galecia.txt`, `email_staff_login.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-028 | Online Hierarchical Cross-Linked Help System | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `interview_sysadmin_2009-05-10.txt`, `evergreen_reference_2009.txt` |
| REQ-029 | User-Friendly Query Designer for Report Construction | Query/Queue | Must Have | `email_report_features.eml` |
| REQ-030 | Report Template Management With Restricted Editable Fields | Query/Queue | Must Have | `email_report_features.eml` |
| REQ-031 | Fine-Grained Report Permissions and Shared Folder Control | Security/Auth | Must Have | `email_report_features.eml`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt` |
| REQ-032 | Predefined Board/Executive Report Templates and Interface | Patron Demographics | Should Have | `email_report_features.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-033 | Report Queue Status, Failure Visibility, and Cancellation Controls | Query/Queue | Must Have | `email_report_features.eml`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt` |
| REQ-034 | Background and Isolated Processing for Long-Running Reports | Query/Queue | Must Have | `meeting_minutes/meeting_2009-07-20_minutes.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt` |
| REQ-035 | Flexible Scheduling and Delivery of Recurring Reports | Query/Queue | Must Have | `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt` |
| REQ-036 | Save and Reuse Query Definitions and Templates | Query/Queue | Must Have | `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt` |
| REQ-037 | Advanced Query Capabilities for Custom Reports | Query/Queue | Must Have | `evergreen_reference_2009.txt` |
| REQ-038 | CSV Excel-Compatible and HTML Report Output | Query/Queue | Should Have | `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt` |
| REQ-039 | Uploaded-Based Filtering for Bulk Identifiers | Query/Queue | Should Have | `evergreen_reference_2009.txt` |
| REQ-040 | Snapshot Historical Reporting and Transaction Retention | Query/Queue | Must Have | `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt` |
| REQ-041 | Grouped Transaction Reporting by Organizational Dimensions | Query/Queue | Must Have | `survey_results_2009.txt` |
| REQ-042 | Count Checkin and Checkout Types Separately | Material Volume | Must Have | `survey_results_2009.txt` |
| REQ-043 | Count Holds by Placement Method | Query/Queue | Must Have | `survey_results_2009.txt` |
| REQ-044 | Anonymized Demographic Statistics by Age and Geography | Patron Demographics | Must Have | `survey_results_2009.txt` |
| REQ-045 | Inclusion of Null and Blank Fields in Results | Query/Queue | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `conversations/conv_pines023_patron_characteristics.eml` |
| REQ-046 | Error Reporting With High-Level and Low-Level Feedback | Query/Queue | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-047 | Report Queue Priority and Queue Jumping | Query/Queue | Must Have | `email_report_features.eml` |
| REQ-049 | Management Reporting Isolated From OPAC Performance | Query/Queue | Must Have | `meeting_tech_subcommittee_2009-06-30.txt`, `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-052 | In-Transit, Missing, and Damaged Reports Support Delivery Coordination | Material Volume | Must Have | `meeting_minutes/meeting_2009-07-20_minutes.txt`, `conversations/conv_pines019_020_missing_intransit.eml`, `interview_cataloging_2009-05-08.txt` |
| REQ-054 | Batch Deletion Utility for Volumes, Copies, and Orphaned Bibliographic Records | Weeding/Purging | Should Have | `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt` |
| REQ-055 | Branch-Specific Weeding and Purging Candidate Reports | Weeding/Purging | Must Have | `meeting_minutes/meeting_2009-07-20_minutes.txt`, `conversations/conv_pines021_item_purging.eml` |
| REQ-056 | Management Reporting and Analysis Tools Include Inventory and Capacity Reporting | Material Volume | Must Have | `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-057 | Cross-Branch Circulation and Inventory Comparison Reports | Query/Queue | Must Have | `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-058 | Linux and Solaris Server Deployment | Query/Queue | Must Have | `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-059 | Financial Reporting and Auditable Financial Tracking | Financial | Must Have | `email_financial_reports.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt` |
| REQ-060 | Financial Reports Compliance, Retention, and Transaction Archive With Privacy Protection | Financial | Must Have | `email_financial_reports.eml`, `email_report_features.eml` |
| REQ-061 | Inventory/Capacity and Shelf Space Reporting Enable Space Allocation Planning | Material Volume | Must Have | `interview_cataloging_2009-05-08.txt`, `conversations/conv_pines016_shelf_space.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt` |
| REQ-062 | Data Specifications and Record Validation Documentation for Management Processes | Query/Queue | Must Have | `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt` |

### Detailed Requirement Specifications

### Requirement REQ-001: Material Volume Report at Point in Time
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines014_material_volume.eml`
- **Subsystem:** Material Volume

The system shall provide a Material Volume Report that calculates and returns material volumes for a specified library at any point in time. The report must separate counts for new acquisitions, items currently checked in (on shelf), and items checked out (in circulation), and include totals plus configurable category breakdowns for monthly and board reporting use.

### Requirement REQ-002: System Capacity Overview Dashboard
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines015_capacity_interface.eml`
- **Subsystem:** Material Volume

The system shall provide a capacity overview interface showing key capacity metrics across branches simultaneously, with the ability to drill down to branch details. It must support sorting and filtering (for example by region, library type, or current load), present trend data for growth/shrink patterns, and support exporting overview data to CSV for external analysis and planning.

### Requirement REQ-003: Shelf Space Versus Usage Comparative Reporting
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines016_shelf_space.eml`
- **Subsystem:** Material Volume

The system shall generate a Shelf Space Report that, for each genre and format, compares three metrics: percentage of total circulations, percentage of the collection, and percentage of total shelf space. The report must run at per-library and per-system levels, support side-by-side comparisons across libraries, and allow time-based filtering such as date range or quarter for reallocation planning.

### Requirement REQ-004: Batch Item Transfer Utility With Preview
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Subsystem:** Query/Queue

The system shall provide a Batch Item Transfer Utility enabling users to build queries to identify candidate materials, save queries for reuse, manually select items from query results, and execute batch transfers to change item locations. It must include a preview of changes before execution, generate pull lists and printable transit labels for moved items, and support undo/revert operations to recover from mistaken transfers.

### Requirement REQ-005: Transfer Authorization, Audit Trail, and History
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines018_item_transfer.eml`
- **Subsystem:** Security/Auth

The system shall restrict transfer operations to authorized roles (for example managers or administrators) and record a complete transfer history for each item. Transfer events must be logged for audit purposes including who initiated the transfer and when it occurred, and also include subsequent reverts so history is queryable for repeated transfers and administrative troubleshooting.

### Requirement REQ-006: Missing and Damaged Items Reporting
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Subsystem:** Material Volume

The system must produce reports enumerating items marked as missing or damaged, grouped by branch to support auditing and collection management. Reports must support selectable date ranges so staff can view recent or historical counts and trends for a specified branch, and include condition notes when available to support diagnosis of damage patterns.

### Requirement REQ-007: In-Transit Items Aging With Merged View
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines019_020_missing_intransit.eml`
- **Subsystem:** Material Volume

The system must generate an in-transit aging report listing items that have been in transit longer than a configurable threshold X days (default suggested as 7). The report must be available per branch and for the entire system and must merge both 'transit-to' and 'transit-from' directions into a single view. It must allow sorting by due date so staff can prioritize oldest items.

### Requirement REQ-008: Item Purging Candidate Identification Report
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Subsystem:** Weeding/Purging

The system should provide read-only reports that identify item records that are candidates for purging based on customizable criteria. Criteria must include status-based rules (for example missing, discard/weed), time-in-status thresholds (for example missing for more than X months), circulation/activity rules (for example not circulated for Y years), and allow combining criteria using AND/OR. The report must only surface candidates without performing deletions.

### Requirement REQ-009: Candidate Reporting and Batch Item Status Conversion
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`, `evergreen_reference_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `conversations/conv_pines022_deletions.eml`, `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`
- **Subsystem:** Weeding/Purging

The system shall provide weeding and deselection reports that identify item candidates using configurable criteria, present those candidates in a read-only view, and support explicit staff-confirmed batch status changes. Supported examples include converting multiple items from “missing” to “discard/weed” or marking selected items for purge, thereby reducing manual effort during branch-level collection maintenance.

### Requirement REQ-010: Last Copy Identification Report for Deletion Safety
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`
- **Subsystem:** Weeding/Purging

The system should provide a last-copy report that identifies items representing the last copy either at a single library or across the consortium/system. The report must allow selecting scope (per library or per system) and must flag records that are the only copy within the selected scope to help catalogers update external catalog records before deletion.

### Requirement REQ-011: Purge and Delete Confirmation Controls With Audit Trail
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `conversations/conv_pines022_deletions.eml`
- **Subsystem:** Weeding/Purging

To prevent accidental data loss, the system must identify purge or delete candidates through a read-only report, require a separate explicit manual confirmation before deletion or batch status changes, and prohibit automated deletion without that confirmation. It must retain an audit trail recording the responsible user, affected records, action, and timestamp for accountability and troubleshooting.

### Requirement REQ-012: Queryable Deletion Logging and Accountability Reports
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines022_deletions.eml`, `survey_results_2009.txt`
- **Subsystem:** Security/Auth

The system must count and log record deletions and, where required for oversight, attempted deletions involving item, patron, bibliographic, or other record types. Each log entry must capture the record type, record identifier, deletion timestamp, responsible user, and user location or branch. Administrators must be able to query and report deletion information by record type, location, and system for auditing and troubleshooting.

### Requirement REQ-013: Patron Demographic Querying and Grouped Aggregations
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`
- **Subsystem:** Patron Demographics

The system should allow reports and queries to be limited (filtered) and grouped (aggregated) by patron characteristics including configurable age ranges computed from birth_date, zip code, county of residence, home branch, patron type, and preferred language. Filters must be combinable with AND/OR logic. Grouping must support aggregates such as counts or circulation by bucket, and results must include records with null values for optional fields rather than silently excluding them.

### Requirement REQ-014: In-Active Patrons Report With Configurable Inactivity
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Patron Demographics

The system must produce a report listing patrons who have had no circulation or electronic activity within a configurable inactivity window, driven by recorded circulation and electronic activity events. Administrators must be able to configure the inactivity cutoff period X days (with examples such as 30, 90, 180, 365, and any other numeric day value).

### Requirement REQ-015: Inactive Patrons Reporting Scope and Data Outputs
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Patron Demographics

The inactive patrons report must support configurable reporting levels so it can be generated at different organizational scopes such as system-wide or by grouping levels like home library and county where supported. The report must include each patron's current mailing address to support outreach, and it should include electronic activity logic by explicitly considering OPAC/patron account logins, online hold placements, online renewals, and access to digital collections when those access events are recorded.

### Requirement REQ-016: CSV Export for Inactive Patrons Report
- **Priority:** Must Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Query/Queue

The system must provide an option to export the inactive patrons report in CSV format so libraries can import lists into external outreach or mailing systems. The CSV export must preserve the included fields such as mailing address, last activity date, and any flags or options applied when generating the report.

### Requirement REQ-017: Background Processing and Caching for Inactive Patrons Report
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines024_inactive_patrons.eml`
- **Subsystem:** Query/Queue

Because the inactivity query may be costly on large patron populations, the system should run the report as a background process and cache results for performance and operational safety. This includes supporting asynchronous generation and storing recent results for reuse.

### Requirement REQ-018: Management Processes Reporting Capabilities Across Enterprise
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`
- **Subsystem:** Query/Queue

The system shall provide consolidated management reporting and analysis tools that allow administrators and managers to analyze operations, collections, branch capacity and distribution, patron demographics and interests, staff productivity and workflow, and financial transactions. Tools must support generation of aggregated and detailed reports used for enterprise-level planning, evaluation, and strategic presentations, usable by Local, Library, and Global administrators.

### Requirement REQ-019: Centralized Multi-Location Management Services
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`
- **Subsystem:** Query/Queue

The Management Processes component shall operate as a centralized service that accepts input from and provides management services to multiple library locations within a consortium. The system must consolidate data and provide centrally-run management functions so administrators can perform system-wide analyses and control while still supporting distributed branch operations.

### Requirement REQ-020: Report and Search Processing During Open Hours
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`
- **Subsystem:** Query/Queue

The system shall support execution of searches and reports during library open hours without disrupting other system functions. This requires managing management-report workloads such that routine patron-facing operations remain responsive while management queries and reports run on the consolidated system.

### Requirement REQ-021: Web Browser and Windows Client Access for Management Tools
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

The system shall be accessible through a web browser or a Windows-compatible client so staff and administrators can reach management tools from typical client environments. The supported access methods must cover the delivery mechanisms for management processes and report generation.

### Requirement REQ-022: Browser Compatibility for Web Interface
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

If the management interface is implemented as a web-based interface, it must provide compatibility with the specified browsers and versions. This includes Microsoft Internet Explorer (version 6.0 and later) and Mozilla Firefox (version 2.0 and later), ensuring common browsers used by library workstations can render and operate the management interfaces.

### Requirement REQ-023: Assistive Technology Support for Management Interfaces
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `interview_sysadmin_2009-05-10.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Patron Demographics

The system shall be accessible using screen-reading software, screen-magnification software, and other assistive technology programs to ensure accessibility for users with disabilities. The management interfaces and online help must be usable via common assistive technology so local and global administrators and staff with accessibility needs can perform required tasks.

### Requirement REQ-024: Relational Database Backend for Management Processes
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

The system shall use a fully relational database back-end to store and manage bibliographic, item, patron, order, hold/request, transaction, and financial records referenced by the Management Processes. This requirement ensures data integrity and queryability while supporting reporting and integration with other ILS modules.

### Requirement REQ-025: Standards-Compliant HTML Output for Web Components
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

Web-based components of the Management Processes shall produce standards-compliant HTML output. This is intended to ensure consistent rendering across browsers, maintainability, and compatibility with assistive technologies so that online help and reporting interfaces work reliably for all users.

### Requirement REQ-026: Development and Training Environment With Migratable Configurations
- **Priority:** Should Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Security/Auth

The system shall provide a development and training environment and support migration of configurations to a production environment. Users must be able to export and import configuration artifacts such as report templates, saved queries, and permission settings between environments to configure and test safely without impacting production data, and then promote validated configurations to production.

### Requirement REQ-027: Role and Group Based Access Control for Management Functions
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `email_staff_login.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Security/Auth

The system shall control user rights and privileges using security groups or role constructs that allow access control for individuals, workgroups, and arbitrary staff groups. It must enable Local System Administrators, Library Managers, Library Administrators, and Global System Administrators to have appropriate and distinct permissions for management functions and reports.

### Requirement REQ-028: Online Hierarchical Cross-Linked Help System
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `interview_sysadmin_2009-05-10.txt`, `evergreen_reference_2009.txt`
- **Subsystem:** Query/Queue

The system shall provide an online, hierarchical, cross-linked help system in HTML that describes and illustrates all system functions. This online help must be accessible from front-end interfaces and provide contextual and navigable documentation for both routine users and administrators.

### Requirement REQ-029: User-Friendly Query Designer for Report Construction
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`
- **Subsystem:** Query/Queue

Provide a query design interface that enables staff to build queries against all record types using selectable fields, picklists, Boolean operators, and selectable regular-expression capabilities. The tool must be user-friendly for staff while allowing administrators to control access to advanced query features, enabling flexible ad hoc and repeatable queries across system data.

### Requirement REQ-030: Report Template Management With Restricted Editable Fields
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`
- **Subsystem:** Query/Queue

Administrators must be able to create, store, and distribute report templates that staff can run as-is or run after making permitted modifications. Templates should be clonable to create variants while preserving originals. The system must allow admins to restrict which filters and display fields can be altered by non-admin users to ensure consistency and protect sensitive fields.

### Requirement REQ-031: Fine-Grained Report Permissions and Shared Folder Control
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`
- **Subsystem:** Security/Auth

Implement fine-grained report permissions administered through roles and security groups so administrators can control who can create, clone, modify, and run reports. Permissions administration must integrate with role changes so changing a user's role updates their report permissions automatically and supports shared folders for controlled report distribution. Additionally, administrators must be able to restrict template creation and execution according to roles and folder-level sharing.

### Requirement REQ-032: Predefined Board/Executive Report Templates and Interface
- **Priority:** Should Have
- **Sources:** `email_report_features.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Patron Demographics

Provide a set of predefined reports intended for board and director use that present basic statistics and activity metrics (for example checkouts, check-ins, holds placed/filled) and allow cross-tabulation by terminal, branch, system, hour, age range, patron type, and patron location. These predefined templates must support common annual reporting needs and be available via an executive/board reporting interface.

### Requirement REQ-033: Report Queue Status, Failure Visibility, and Cancellation Controls
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`, `survey_results_2009.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`
- **Subsystem:** Query/Queue

The system must queue report jobs and show users their submission timestamp, queue position or processing state, and status such as waiting, running, completed, or failed. It must display failure reasons and allow users or administrators to cancel scheduled or currently running reports. The processing engine must check cancellation signals during execution so long-running jobs can stop in a controlled manner.

### Requirement REQ-034: Background and Isolated Processing for Long-Running Reports
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`, `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`
- **Subsystem:** Query/Queue

The system shall process large or complex reports as queued or background work without degrading primary functions such as OPAC and circulation. It should support scheduled execution, avoid tying up production resources during peak interactive use, and may use read-only reporting replicas where appropriate. The design should remain compatible with PostgreSQL architecture and PINES server environments when required.

### Requirement REQ-035: Flexible Scheduling and Delivery of Recurring Reports
- **Priority:** Must Have
- **Sources:** `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`
- **Subsystem:** Query/Queue

Users must be able to schedule reports to run at configurable intervals including ASAP, hourly, daily, weekly, monthly, and yearly, and specify delivery mechanisms such as direct download or email delivery. Saved schedules should support recurring execution and include basic run-time options for operational automation.

### Requirement REQ-036: Save and Reuse Query Definitions and Templates
- **Priority:** Must Have
- **Sources:** `evergreen_reference_2009.txt`, `interview_cataloging_2009-05-08.txt`, `survey_results_2009.txt`
- **Subsystem:** Query/Queue

The system must allow staff to save query definitions and report templates for repeated use, allow editing of saved templates, and provide mechanisms for organizing and reusing those templates. This enables recurring workflows such as monthly transfers and repeated weeding queries without reconstructing complex selection criteria each time.

### Requirement REQ-037: Advanced Query Capabilities for Custom Reports
- **Priority:** Must Have
- **Sources:** `evergreen_reference_2009.txt`
- **Subsystem:** Query/Queue

The reporting interface must support constructing complex queries beyond simple filters, including Boolean combinations and access to a broad set of reportable fields. This capability is required so staff can produce sophisticated reports that cannot be expressed with limited query constructs or overly restricted field selection.

### Requirement REQ-038: CSV Excel-Compatible and HTML Report Output
- **Priority:** Should Have
- **Sources:** `evergreen_reference_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`
- **Subsystem:** Query/Queue

Reports must be exportable in CSV, Excel-compatible or Excel format, and HTML. CSV shall support reliable raw-data extraction, Excel output shall support business-user analysis including pivot-table workflows, and HTML shall support web display. Providing these formats enables downstream analysis and allows users to consume results through machine-oriented or presentation-oriented workflows.

### Requirement REQ-039: Uploaded-Based Filtering for Bulk Identifiers
- **Priority:** Should Have
- **Sources:** `evergreen_reference_2009.txt`
- **Subsystem:** Query/Queue

The system should accept uploaded text files (for example lists of barcodes or other identifiers) to be used as selection filters for reports and batch operations. This supports running reports or batch moves against externally-defined sets of items without manual per-item selection.

### Requirement REQ-040: Snapshot Historical Reporting and Transaction Retention
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`, `meeting_tech_subcommittee_2009-06-30.txt`
- **Subsystem:** Query/Queue

The system shall maintain transaction history for a configurable retention period X days and retain monthly and annual aggregates indefinitely to support historical reporting. Users must be able to generate reports that reflect the system state on a specified past date so snapshot-style historical queries can be produced even if shelving locations or other attributes changed since that date.

### Requirement REQ-041: Grouped Transaction Reporting by Organizational Dimensions
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`
- **Subsystem:** Query/Queue

Transaction reports must support grouping and aggregation by hour, terminal, branch, library group, system, and county. The reporting results shall provide totals at applicable time, service-point, organizational, and geographic levels, enabling staff to identify busy periods, compare activity among operating units, and analyze transaction volume across the specified dimensions for planning and management purposes.

### Requirement REQ-042: Count Checkin and Checkout Types Separately
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`
- **Subsystem:** Material Volume

Reports must distinguish and count different types of check-ins and check-outs separately, such as book-drop versus terminal versus self-service check-ins, and staff checkout versus self checkout plus renewal types. Aggregates across all types should also be available for cumulative metrics.

### Requirement REQ-043: Count Holds by Placement Method
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`
- **Subsystem:** Query/Queue

Hold reports shall include the method of placement (for example at staff desk, at public computer, or remotely) so holds and related statuses (fills, stale holds) can be analyzed with placement context. This requires storing and surfacing placement method on hold events.

### Requirement REQ-044: Anonymized Demographic Statistics by Age and Geography
- **Priority:** Must Have
- **Sources:** `survey_results_2009.txt`
- **Subsystem:** Patron Demographics

Demographic reporting shall provide aggregated statistics by geographical region and age range while protecting patron privacy. The system must prevent personally identifiable information from being exposed in these reports and must present results at a level suitable for program planning, service analysis, and comparison of demographic patterns without revealing individual patron identities or records.

### Requirement REQ-045: Inclusion of Null and Blank Fields in Results
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `survey_results_2009.txt`, `conversations/conv_pines023_patron_characteristics.eml`
- **Subsystem:** Query/Queue

Report results shall explicitly include null and blank fields so missing data remains visible to users. The system must not prune or omit rows/columns solely because fields are null; null-handling must preserve the presence of blanks as part of the returned dataset.

### Requirement REQ-046: Error Reporting With High-Level and Low-Level Feedback
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

When reports fail, the system must provide thorough high-level error reporting for users and low-level query-specific feedback for administrators. Admin diagnostics must expose actionable information so staff can troubleshoot failures, including details sufficient to identify where the failure occurred and why.

### Requirement REQ-047: Report Queue Priority and Queue Jumping
- **Priority:** Must Have
- **Sources:** `email_report_features.eml`
- **Subsystem:** Query/Queue

The system must provide functionality allowing authorized users or high-priority report types to be elevated in the reporting queue so important reports (for example board reports) can execute ahead of lower-priority ad-hoc queries. The system must support prioritization controls that can change a job’s queue priority when operationally necessary.

### Requirement REQ-049: Management Reporting Isolated From OPAC Performance
- **Priority:** Must Have
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`, `early_draft_srs_galecia.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Management Processes shall exchange data with the Online Public Access Catalog where needed to support reporting and related management workflows, but they shall not constrain, alter, or limit OPAC module functionality. Reporting activities must be separated or otherwise controlled so they do not slow public catalog responsiveness or degrade patron-facing services during normal use.

### Requirement REQ-052: In-Transit, Missing, and Damaged Reports Support Delivery Coordination
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`, `conversations/conv_pines019_020_missing_intransit.eml`, `interview_cataloging_2009-05-08.txt`
- **Subsystem:** Material Volume

The system shall provide reports that support collection health monitoring and delivery coordination between branches, including an in-transit item reporting capability and missing/damaged reporting broken down by branch. These reports should help staff locate lost transfers between branches and support local inventory reconciliation and remedial action planning.

### Requirement REQ-054: Batch Deletion Utility for Volumes, Copies, and Orphaned Bibliographic Records
- **Priority:** Should Have
- **Sources:** `conversations/conv_pines021_item_purging.eml`, `interview_cataloging_2009-05-08.txt`
- **Subsystem:** Weeding/Purging

The system should provide a quick utility for batch deletion of volume records together with associated copy/item entries, and for removal of bibliographic records that have no item attachments. The utility must present identified records in a non-destructive manner first (listing or preview) and require explicit confirmation before deletion.

### Requirement REQ-055: Branch-Specific Weeding and Purging Candidate Reports
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`, `conversations/conv_pines021_item_purging.eml`
- **Subsystem:** Weeding/Purging

The system shall provide weeding and deselection reports for collection maintenance that identify withdrawal or purge candidates according to agreed criteria. Reports must support branch-specific candidate lists so librarians can review shelf content, manage collection quality, and organize withdrawal activities appropriately for each participating location while retaining the reporting focus on actionable maintenance decisions.

### Requirement REQ-056: Management Reporting and Analysis Tools Include Inventory and Capacity Reporting
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Material Volume

Management Processes shall include inventory and capacity reports that allow staff to analyze collection size, branch-level holdings, and capacity utilization, and support decisions about distribution and shelving. These reports are expected to be used frequently, including daily, for branch-level inventory management.

### Requirement REQ-057: Cross-Branch Circulation and Inventory Comparison Reports
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

The reporting tool shall support comparison reports across branches for circulation, inventory, and other available metrics. Results must allow managers to examine differences between locations and evaluate relative performance and capacity, providing information useful for collection redistribution, operational planning, and management decisions involving multiple branches within the organization.

### Requirement REQ-058: Linux and Solaris Server Deployment
- **Priority:** Must Have
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Query/Queue

Management Processes shall be deployable and operable on Linux or Solaris server operating systems. Reporting components must support production deployment on either server platform used by PINES member installations, allowing the management-processing environment to run on the applicable operating system without restricting deployment to only one of these supported server platforms.

### Requirement REQ-059: Financial Reporting and Auditable Financial Tracking
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`, `meeting_minutes/meeting_2009-03-15_minutes.txt`, `meeting_minutes/meeting_2009-07-20_minutes.txt`, `survey_results_2009.txt`
- **Subsystem:** Financial

The system must provide financial reporting to track and verify financial transactions with branch-level and system-level financial data necessary for budgeting, audits, and director-level oversight. It must include an auditable ledger of all patron payments linked to charges for reconciliation and audit, and support reporting on balances and accrued fines/charges with time-series and category breakdowns, including waived fines by branch and period.

### Requirement REQ-060: Financial Reports Compliance, Retention, and Transaction Archive With Privacy Protection
- **Priority:** Must Have
- **Sources:** `email_financial_reports.eml`, `email_report_features.eml`
- **Subsystem:** Financial

All financial reports and archived financial data must comply with standard accounting practices and applicable auditing and retention requirements, supporting archiving and retention policies and authorized retrieval. The system must maintain an archive of transactional records that preserves the ability to produce permitted statistics while protecting patron privacy per applicable state law, supporting required retention periods.

### Requirement REQ-061: Inventory/Capacity and Shelf Space Reporting Enable Space Allocation Planning
- **Priority:** Must Have
- **Sources:** `interview_cataloging_2009-05-08.txt`, `conversations/conv_pines016_shelf_space.eml`, `meeting_minutes/meeting_2009-07-20_minutes.txt`
- **Subsystem:** Material Volume

The reporting system must provide collection development and space allocation decision support by including material volume reporting and shelf space utilization analyses. These outputs should support assessment of physical shelving use and enable planning actions such as weeding, redistributing, or changing collection allocations based on quantified relationships between usage and shelf space.

### Requirement REQ-062: Data Specifications and Record Validation Documentation for Management Processes
- **Priority:** Must Have
- **Sources:** `early_draft_srs_galecia.txt`, `meeting_tech_subcommittee_2009-06-30.txt`, `meeting_minutes/meeting_2009-03-15_minutes.txt`
- **Subsystem:** Query/Queue

The developer shall provide complete data specifications and data dictionaries for authority records, bibliographic records, order records, item records, hold/request records, and other records used by Management Processes. Additionally, provide high-level process descriptions (e.g., bibliographic import/export and validation) and ensure online hierarchical help in accessible HTML is provided to assist staff.

# Blacklist: Discarded and Contradictory Proposals

This section documents stakeholder suggestions and early draft proposals that were analyzed by the agentic network and discarded or rejected due to architectural conflict, privacy policy, or resource constraints (satisfying OS9).

### Blacklist Item BLK-001: Won't Have: Automated Purging Without Confirmation
- **Rationale:** Rejected because it contradicts the accepted purge workflow requiring read-only candidate reporting, a separate explicit confirmation step, and audit trails to prevent accidental mass data loss.
- **Sources:** `conversations/conv_pines021_item_purging.eml`

### Blacklist Item BLK-002: Won't Have: Exclude Null Values From Demographic Reports
- **Rationale:** Rejected because it conflicts with the consolidated requirement that demographic reports must include records with null optional fields so missing data remains visible and reports do not silently misrepresent populations.
- **Sources:** `conversations/conv_pines023_patron_characteristics.eml`

### Blacklist Item BLK-003: Do Not Constrain OPAC Functionality
- **Rationale:** Explicitly rejected proposal; it is stated as an OPAC constraint that will not be implemented as part of Management Processes requirements, and therefore is not an active requirement to include.
- **Sources:** `early_draft_srs_galecia.txt`

### Blacklist Item BLK-004: Rejected: Run Reports Directly on Production Database
- **Rationale:** Explicitly rejected; the documentation states executing complex reports directly on production transactional database is problematic because it can tie up resources and slow patron-facing services.
- **Sources:** `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`

### Blacklist Item BLK-005: Rejected: No Accessibility Compliance
- **Rationale:** Explicitly rejected; the sysadmin states accessibility is mandatory and therefore a non-accessible reporting UI is unacceptable and must not be implemented.
- **Sources:** `interview_sysadmin_2009-05-10.txt`

### Blacklist Item BLK-006: Rejected: No Background Processing for Long-Running Reports
- **Rationale:** Explicitly rejected; interviews state lack of background processing causes performance degradation of OPAC and circulation clients, so this approach must not be adopted.
- **Sources:** `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`

### Blacklist Item BLK-007: Rejected: No Role-Based Report Permission Controls
- **Rationale:** Explicitly rejected because it contradicts required fine-grained report permission controls distinguishing who can create, edit, save, and run reports and how permissions are administered.
- **Sources:** `evergreen_reference_2009.txt`, `interview_sysadmin_2009-05-10.txt`

### Blacklist Item BLK-008: Rejected: Denormalize Production Database For Reporting
- **Rationale:** Explicitly rejected; technical subcommittee advises against denormalization because maintaining synchronized denormalized copies creates more problems than it solves.
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`

### Blacklist Item BLK-009: Rejected: Allow Reporting To Constrain OPAC Performance
- **Rationale:** Explicitly rejected; the meeting states reporting must be separate from public catalog and must not slow or impact OPAC responsiveness for patrons.
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`

### Blacklist Item BLK-010: Rejected: Provide Only Generic Error Messages
- **Rationale:** Explicitly rejected; the requirement is for actionable diagnostics and meaningful high-level feedback rather than only generic errors like 'query failed'.
- **Sources:** `meeting_tech_subcommittee_2009-06-30.txt`

### Blacklist Item BLK-011: Support for Streamlined Staff Login Methods (Rejected)
- **Rationale:** Explicitly rejected proposal to require streamlined login methods as mandatory; consensus is that streamlined login should be supported but not mandatory due to hardware availability differences.
- **Sources:** `email_staff_login.eml`

### Blacklist Item BLK-012: Permit Card-swipe to Bypass Authentication (Rejected)
- **Rationale:** Explicitly rejected; card-swipe must still map to and record the individual staff member for auditing, so anonymous or bypassed logins are not acceptable.
- **Sources:** `email_staff_login.eml`

### Blacklist Item BLK-013: Unrestricted Template Modification by Staff (Rejected)
- **Rationale:** Explicitly disallowed; non-admin staff must not be allowed to freely modify admin-controlled report templates because protected fields and consistency would be compromised.
- **Sources:** `email_report_features.eml`

### Blacklist Item BLK-014: Exclude Patron Facing OPAC Functions
- **Rationale:** Explicitly rejected scope limitation: it states OPAC patron-facing functions belong to OPAC and must be excluded as out of scope; this contradicts the active requirement to interact with OPAC.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`

### Blacklist Item BLK-015: Do Not Constrain OPAC Functionality
- **Rationale:** Explicitly rejected duplicate OPAC constraint proposal; stated as explicitly rejected and excluded from implementation as part of Management Processes.
- **Sources:** `meeting_minutes/meeting_2009-07-20_minutes.txt`, `early_draft_srs_galecia.txt`

### Blacklist Item BLK-016: Defer Detailed UI Specification Now
- **Rationale:** Explicitly rejected; detailed UI specification for reports and administrative screens is deferred and therefore excluded from the active requirement set.
- **Sources:** `meeting_minutes/meeting_2009-03-15_minutes.txt`
