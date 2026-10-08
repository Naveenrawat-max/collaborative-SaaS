---
title: "Architecture"
tags:
  - kind/doc
  - area/architecture
  - status/current
---

# Architecture

This note summarises section 4 of [[specs/001-rfid-wms-pilot-design]].

Decisions it follows:
- [[_meta/decisions/001-stack-django-react]]
- [[_meta/decisions/002-multi-tenancy]]
- [[_meta/decisions/003-api-drf]]
- [[_meta/decisions/004-native-operator-app-trc-rfid]]
- [[_meta/decisions/005-tag-identity-epc-tid-qr]]

## Components

```
 Operator: Chainway C72                      Back office: desktop browser
 ┌───────────────────────────────┐           ┌───────────────────────┐
 │ Native Kotlin app (Compose)   │           │ React web app         │
 │  screens → domain logic       │           │ admin + manager       │
 │  trc-rfid: RfidScanner,       │           └──────────┬────────────┘
 │            TagFinder          │                      │
 │  QR via Keyboard Emulator     │                      │
 └──────────────┬────────────────┘                      │
                └────────── HTTPS JSON /api/v1 ─────────┘
                       Django + DRF, single movement service
                                    │
                                PostgreSQL
                                    ▲
        Phase 2: edge gateway (Python + sllurp, on-site mini-PC)
                 LLRP dock readers → filter → events → API
```

| Component | Path | Notes |
|---|---|---|
| Django API | `backend/` | DRF under `/api/v1`, tenant-scoped base viewset, OpenAPI via drf-spectacular |
| React back office | `web/` | admin + manager screens (tooling still open, see [[STATE]]) |
| Operator app | `android/` | Kotlin + Compose, `trc-rfid:rfid-find:1.0.0`, QR via Keyboard Emulator (QR-only) |
| Edge gateway | `gateway/` | **Phase 2** — Python + `sllurp`, buffers events when the link to the API is down |
| Docs vault | `wms-docs/` | this vault |

Create each folder when its first code lands, not before.

## Rule: raw reads never reach the server

1. `RfidScanner.onTag` delivers raw reads, many per second per tag.
2. The app de-duplicates them by EPC and attaches the TID once a read delivers it.
3. The app matches tags live against the expected list: ✅ matched / ⚠ unexpected / ❌ missing.
4. The operator confirms. The app sends **one business transaction** with a
   `txn_id`, e.g. `POST /api/v1/receipts/{id}/confirm`.
5. The server does it all in one DB transaction:
   1. resolves the tags (same tenant)
   2. binds the pallets
   3. calls the movement service
   4. writes `Scan` rows
   5. returns a result per tag
6. A repeated `txn_id` is applied only once, so retry after a network drop is safe.

The Phase 2 gateway follows the same rule: filter at the dock and send events.

## Auth
- **Back office:** session login.
- **Handheld:**
  1. An admin registers the device to one warehouse.
  2. The operator logs in with username + PIN.
  3. The app receives a short-lived token.

## Code map
Once code exists, decide how `tools/vaultify.py sync` writes code notes into this
vault (open item in [[STATE]]).
