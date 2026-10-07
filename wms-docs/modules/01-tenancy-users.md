---
title: "Module 01 — Tenancy & users"
tags:
  - kind/doc
  - area/tenancy
  - status/draft
---

# Module 01 — Tenancy & users

Who can sign in, which tenant they belong to, and what they may do. Every other
module depends on this one. Isolation model: [[_meta/decisions/002-multi-tenancy]].
Permissions: [[roles-permissions]].

- **Owner:** _TBD_ (proposed: dev C) · **Milestone:** M0 — see [[roadmap]]
- **Status:** draft scope — confirm before writing the spec

## In scope
- Tenant lifecycle: create (by platform staff), suspend, reactivate, and tenant settings (timezone, units, **RFID enabled on/off**).
- Users: invite by email, activate, deactivate, reset password.
- Roles `admin`, `manager`, and `operator`, assigned per user.
- **Warehouse access**: a user is limited to specific warehouses (managers and operators).
- Login for web, and quick login for handheld (e.g. badge scan + PIN — open question).
- Audit of security events: login, failed login, role change.

## Out of scope (for now)
SSO/SAML, self-service tenant sign-up, billing and subscriptions, custom roles.

## Key entities
`Tenant`, `User`, `Membership` (user ↔ tenant + role), `WarehouseAccess`, `TenantSettings`.

## Main flows
1. Platform staff creates a tenant and its first `admin`.
2. The admin invites users, assigns a role and warehouses.
3. A user logs in and only sees their tenant and permitted warehouses.

## Used by
Every module. Tenant scoping is mandatory everywhere (AGENTS.md invariant 1).

## Open questions
- Can one user belong to several tenants (e.g. a 3PL staff member)?
- Is there a platform super-admin UI, or is the Django admin enough at first?
- Handheld login method: username/password, badge + PIN, or device-bound session?
