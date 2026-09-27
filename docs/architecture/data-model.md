# Aegis — Data Model

**Version:** 0.1  
**Status:** Draft

## 1. Purpose

This document defines the logical data model for Aegis and acts as the
blueprint for the Bronze, Silver, and Gold data layers.

---

## 2. Core Entities

### Dimensions

- Customer
- Product
- Supplier
- Warehouse
- Carrier

### Relationship

- Supplier Product

### Facts

- Order
- Order Item
- Shipment
- Shipment Item
- Inventory Snapshot
- Return

---

## 3. Entity Relationships

```text
Customer
   │
   └── 1:N ──► Order
                  │
                  └── 1:N ──► Order Item
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
                 Product       Supplier     Shipment Item
                                                │
                                                ▼
                                             Shipment
                                             /      \
                                            ▼        ▼
                                       Warehouse   Carrier

Product ──┐
          ├──► Inventory Snapshot ◄── Warehouse
          │
Supplier ─┴──► Supplier Product