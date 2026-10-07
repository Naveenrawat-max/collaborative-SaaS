---
title: "Module 09 — Integrations & labels"
tags:
  - kind/doc
  - area/integrations
  - status/draft
---

# Module 09 — Integrations & labels

How data gets in and out of the WMS, and how labels get printed. It feeds ASNs
into [[modules/04-inbound-receiving]] and orders into [[modules/07-outbound]].

- **Owner:** _TBD_ · **Milestone:** M1 (labels, CSV), M5 (API, webhooks) — see [[roadmap]]
- **Status:** draft scope

## In scope
- **CSV import/export**: items, locations, ASNs, orders, and a stock snapshot.
  Validate, preview, then commit, with a row-level error report.
- **REST API** for customers' ERP and e-commerce systems: ASNs and orders in;
  receipts, shipments, and stock out. Uses per-tenant API keys.
- **Webhooks**: notify the customer's system on receipt closed, shipment
  dispatched, or stock adjusted.
- **Labels**: LPN, location, and item labels as PDF first; ZPL for Zebra printers
  next. Printing from the browser or to a network printer.
- **Documents**: packing list, delivery note.

## Out of scope (for now)
Built-in connectors for specific ERPs (SAP, Odoo, Shopify…) — they come later,
driven by customer demand.

## Key entities
`ImportJob`, `ApiKey`, `WebhookEndpoint`, `WebhookDelivery`, `LabelTemplate`.

## Open questions
- Which ERP or e-commerce systems do the first customers use?
- Is EDI (e.g. DESADV ASN) needed?
- Print path: browser print dialog, or direct to a network printer (needs an on-site agent)?
