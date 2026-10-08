---
title: "Module 10 — Reporting & audit"
tags:
  - kind/doc
  - area/reporting
  - status/draft
---

# Module 10 — Reporting & audit

Visibility for managers and admins, and a complete trail of who did what. Most
data comes from the `Movement` and event records in [[modules/06-inventory]]
and [[modules/03-vehicles-yard]].

- **Owner:** _TBD_ (shared) · **Milestone:** M5 (dashboards), audit from M0 — see [[roadmap]]
- **Status:** draft scope

## In scope
- **Audit log** (from M0): every create, update, or delete on business records and
  every security event — user, tenant, time, before/after. Append-only. See
  [[non-functional]].
- **Operational dashboards**: today's inbound and outbound, open tasks, dock and
  yard status, exceptions (discrepancies, short picks).
- **Reports**: stock on hand, by-location stock, movement history, expiry, receipt
  and shipment history, cycle-count accuracy, dock dwell time, operator productivity.
- **RFID health:** QR fallback rate (target < 2%), tag conflicts, and unreadable
  tags flagged — per site and per device.
- CSV export of every report.

## Out of scope (for now)
Custom report builder, BI tool integration, and scheduled email reports.

## Open questions
- Which three reports do first customers need on day one?
- How long is audit data retained, and is that legally required per country?
