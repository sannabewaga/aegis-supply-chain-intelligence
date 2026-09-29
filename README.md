# Aegis: Agentic Supply Chain Intelligence Platform

> An AI-powered supply-chain decision-support platform built on Databricks, combining Data Engineering, Generative AI, Enterprise RAG, and agentic investigation.

![Databricks](https://img.shields.io/badge/Databricks-Unity%20Catalog-FF3621)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-Medallion-00ADD4)
![Gemini](https://img.shields.io/badge/LLM-Gemini%203.5%20Flash%20Lite-4285F4)
![Python](https://img.shields.io/badge/Python-PySpark-3776AB)

## Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [Architecture](#architecture)
- [Data Architecture](#data-architecture)
- [Synthetic Data: AegisMart](#synthetic-data-aegismart)
- [Incident Simulation](#incident-simulation)
- [Agent Architecture](#agent-architecture)
- [Analytical Tool Layer](#analytical-tool-layer)
- [Enterprise RAG](#enterprise-rag)
- [Evidence Discipline](#evidence-discipline)
- [Example Investigation](#example-investigation)
- [Design Principles](#design-principles)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Security](#security)
- [Current Status](#current-status)

---

## Overview

**Aegis** is an end-to-end supply-chain intelligence platform that helps operations teams monitor performance, investigate disruptions, retrieve operational policies, and reason about potential root causes.

It combines:

- Lakehouse data engineering (Delta Lake, Unity Catalog, Medallion Architecture)
- Parameterized Unity Catalog analytical functions
- Enterprise RAG with Databricks AI Search
- Gemini-powered agentic reasoning with multi-step tool calling
- Synthetic enterprise-scale data with ground-truth operational incidents
- Evidence-grounded investigation

The core workflow is:

**MONITOR → INVESTIGATE → SIMULATE → DECIDE**

Aegis is a **decision-support system**, not an autonomous operational control system.

---

## The Problem

Supply-chain teams rarely lack data. The problem is connecting that data into an investigation.

A question such as:

> "Why did supplier SUP0014 deteriorate in February?"

may require examining:

- Supplier performance and historical trends
- Supplier-to-warehouse relationships
- Warehouse and carrier performance
- Inventory consequences
- SLA policies and escalation guidelines

Traditional dashboards surface individual metrics but don't connect these pieces of evidence into a structured investigation. Aegis gives an AI agent access to **controlled analytical tools and enterprise knowledge** so it can do that work.

---

## Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         │ Natural-language     │
                         │ business question    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Aegis Agent       │
                         │  Gemini 3.5 Flash    │
                         │        Lite          │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ UC Analytical  │ │ Enterprise RAG │ │ Supplier       │
        │ Functions      │ │ Databricks AI  │ │ Network Tool   │
        │                │ │ Search         │ │                │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │ Evidence Synthesis   │
                         │ Facts + Policies +   │
                         │ Context + Reasoning  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Grounded Answer      │
                         │ with investigation   │
                         │ trace                │
                         └──────────────────────┘
```

---

## Data Architecture

Aegis follows a Medallion Architecture:

```text
Raw Parquet
    │
    ▼
┌───────────────┐
│ Bronze        │  Raw, source-aligned Delta tables in Unity Catalog
└───────┬───────┘
        ▼
┌───────────────┐
│ Silver        │  Cleaned, standardized, source-grain tables
└───────┬───────┘
        ▼
┌───────────────┐
│ Gold          │  Business performance models
└───────┬───────┘
        ▼
┌───────────────┐
│ AI / Agent    │
│ Tool Layer    │
└───────────────┘
```

| Layer | Contents |
|-------|----------|
| **Bronze** | Raw source-aligned Delta tables stored in Unity Catalog |
| **Silver** | Deterministic derived fields: revenue, actual transit days, delivery delay, late-delivery flag, available inventory, stockout flag |
| **Gold** | Supplier performance, delivery performance, inventory health, warehouse performance, carrier performance, supply-chain risk signals |

The Gold layer contains deterministic analytical logic and does not depend on the LLM.

---

## Synthetic Data: AegisMart

Aegis uses a synthetic enterprise environment called **AegisMart**, a fictional mid-sized Indian e-commerce retailer.

| Entity | Records |
|--------|--------:|
| Customers | 20,000 |
| Products | 1,000 |
| Suppliers | 50 |
| Supplier-Products | 4,504 |
| Warehouses | 10 |
| Carriers | 10 |
| Orders | 300,000 |
| Order Items | 659,466 |
| Shipments | 328,195 |
| Shipment Items | 663,865 |
| Inventory Snapshots | 5,480,000 |
| Returns | 41,620 |
| Ground-truth incidents | 5 |

The dataset spans **18 months (548 days)** and can be regenerated deterministically using a fixed seed.

---

## Incident Simulation

Instead of adding obvious `incident_flag` columns, operational incidents are injected into the underlying behavior of the system. Aegis must investigate incidents from their **observable consequences** rather than reading a hidden label.

| ID | Area | Period |
|----|------|--------|
| INC001 | Supplier SUP0014 degradation | Jan–Apr 2025 |
| INC002 | Warehouse WH0003 bottleneck | Nov 2024–Jan 2025 |
| INC003 | Carrier CAR0007 degradation | May–Jul 2025 |
| INC004 | Electronics demand shock | Feb–Mar 2025 |
| INC005 | Product-level inventory anomaly | Aug–Sep 2024 |

Ground truth is retained separately for validation and analysis.

---

## Agent Architecture

The Aegis agent uses a multi-step tool-calling loop:

```text
User Question
      │
      ▼
   Gemini
      │
      ├── Analytical Tool
      ├── RAG Search
      ├── Supplier Network
      └── Additional Analytical Tools
             │
             ▼
        Tool Results
             │
             ▼
          Gemini
             │
             ▼
       Final Answer
```

The agent can perform multiple investigation steps rather than relying on a single model call. A maximum step limit is enforced as a safety control.

---

## Analytical Tool Layer

The agent does **not** receive unrestricted database access. Instead, it uses controlled Unity Catalog functions:

```text
get_supplier_performance()
get_delivery_performance()
get_inventory_health()
get_warehouse_performance()
get_carrier_performance()
get_supply_chain_risk()
get_supplier_network()
```

This provides a controlled interface between the LLM and the analytical layer:

```text
Gemini
  │  "Investigate SUP0014"
  ▼
get_supplier_performance()
  │
  ▼
Deterministic SQL result
  │
  ▼
Gemini interprets evidence
```

The LLM does not invent the underlying business metrics.

---

## Enterprise RAG

Aegis includes an enterprise knowledge layer of operational policies and metric definitions:

- Supplier SLA Policy
- Warehouse Operations Policy
- Carrier SLA Policy
- Inventory Policy
- Returns Policy
- Supply Chain Escalation Policy
- Metric Definitions

Retrieval pipeline:

```text
Markdown Documents
       ↓
Document Chunking
       ↓
Databricks AI Search
       ↓
Hybrid Retrieval
       ↓
Agent Context
```

The knowledge base contains **48 meaningful chunks**.

---

## Evidence Discipline

Aegis explicitly separates different levels of evidence:

```text
Observed fact
     ↓
Documented policy
     ↓
Correlation
     ↓
Plausible explanation
     ↓
Confirmed evidence
```

The agent is instructed not to convert correlation into causation automatically. For example:

> A supplier's late-delivery rate increased at the same time as warehouse delays.

does **not** automatically mean:

> The supplier caused the warehouse delays.

The agent investigates relevant warehouse and carrier context before drawing conclusions.

---

## Example Investigation

**Question:** *Why did supplier SUP0014 deteriorate in February 2025?*

The agent can combine:

```text
Supplier Performance
        ↓
Supplier Network
        ↓
Warehouse Performance
        ↓
Carrier Performance
        ↓
Supply-chain Risk
        ↓
Enterprise Policies
        ↓
Evidence Synthesis
```

For SUP0014, February 2025 supplier performance showed a substantial deterioration in late deliveries compared with January. The investigation then examines the operational network associated with the supplier rather than stopping at the supplier-level metric.

---

## Design Principles

**Deterministic systems calculate facts.**
Spark, SQL, and Unity Catalog functions are responsible for metrics, aggregations, relationships, derived fields, risk signals, and scenario calculations.

**GenAI interprets and orchestrates.**
Gemini understands user intent, selects tools, combines evidence, retrieves relevant policies, explains findings, and conducts multi-step investigations.

**No invented business metrics.**
The model should not fabricate numerical values that can be obtained from the analytical layer.

**Controlled tool access.**
The agent interacts with predefined analytical functions rather than arbitrary database queries.

**Decision support, not autonomous control.**
Aegis provides evidence and analysis for human decision-makers. It does not automatically execute operational actions.

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| **Data Engineering** | Python, PySpark / Spark SQL, Delta Lake, Databricks, Unity Catalog, Medallion Architecture |
| **AI / GenAI** | Gemini API (Gemini 3.5 Flash Lite), Databricks AI Search, Hybrid Retrieval, Enterprise RAG, Function Calling, Agentic Workflows |
| **Data** | Synthetic enterprise data, Parquet, Delta tables |
| **Development** | GitHub, Databricks Git Folders, Python, SQL, Streamlit |

---

## Repository Structure

```text
aegis-supply-chain-intelligence/
│
├── app/
│   ├── app.py
│   ├── app.yaml
│   ├── requirements.txt
│   └── README.md
│
├── data_generator/
│   ├── config.py
│   ├── generate_all.py
│   ├── generate_dimensions.py
│   ├── generate_inventory.py
│   ├── generate_transactions.py
│   ├── inject_incidents.py
│   ├── validate_data.py
│   └── README.md
│
├── databricks/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── ai/
│       ├── agent/
│       ├── rag/
│       ├── tools/
│       └── visualization/
│
├── docs/
│   ├── product/
│   └── architecture/
│
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## Getting Started

### 1. Generate the data

Install dependencies:

```bash
pip install pandas numpy pyarrow
```

Generate the complete dataset:

```bash
python data_generator/generate_all.py
```

The generator writes Parquet datasets under `data/`.

The validation pipeline checks:

- Primary-key uniqueness
- Foreign-key validity and referential integrity
- Positive quantities
- Price/cost relationships
- Shipment consistency and delivery dates
- Return validity
- Incident propagation

### 2. Databricks setup

Load the generated Parquet datasets into a Unity Catalog volume. The project uses the following schemas:

```text
workspace
├── aegis_bronze
├── aegis_silver
├── aegis_gold
└── aegis_ai
```

- `aegis_gold` exposes the analytical functions.
- `aegis_ai` holds the RAG layer:
  - `workspace.aegis_ai.document_chunks`
  - `workspace.aegis_ai.aegis_index`

---

## Security

Secrets are not stored in the repository. The Gemini API key is stored in a Databricks secret scope:

```text
aegis-secrets
└── gemini-api-key
```

No API credentials are committed to Git.

---

