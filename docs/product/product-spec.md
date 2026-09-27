# Aegis — Product Specification

**Version:** 0.1  
**Status:** Draft  
**Platform:** Databricks Free Edition  
**Project Type:** Agentic Supply Chain Intelligence Platform

---

## 1. Product Overview

Aegis is an agentic supply chain intelligence platform that combines structured
supply-chain analytics, enterprise knowledge retrieval, generative AI, and
scenario analysis.

The platform is designed to help supply-chain and operations users:

1. Monitor operational performance.
2. Investigate anomalies and disruptions.
3. Retrieve relevant enterprise policies and operational knowledge.
4. Analyze operational risks.
5. Simulate business scenarios.
6. Generate evidence-grounded explanations.
7. Explore analytical results through natural-language queries and
   visualizations.

Aegis is designed as a production-oriented portfolio system using the
Databricks platform and its native data and AI capabilities.

---

## 2. Problem Statement

Supply-chain data is distributed across multiple operational domains:

- Orders
- Products
- Suppliers
- Inventory
- Warehouses
- Shipments
- Deliveries
- Carriers
- Returns

Operational knowledge is also distributed across unstructured documents:

- Supplier policies
- Contracts
- Standard operating procedures
- Delivery SLAs
- Procurement policies
- Incident reports
- Business definitions

Traditional dashboards can show that a problem exists, but they often require
an analyst to manually investigate why it happened.

Operational analysts may also need to move between multiple systems to answer
a single business question.

For example:

> Why did on-time delivery fall this week?

Answering this may require:

- querying delivery data,
- comparing historical performance,
- identifying affected warehouses,
- identifying affected suppliers,
- reviewing incident records,
- checking operational policies,
- and interpreting the results.

Aegis aims to reduce this investigation effort by combining structured
analytics with enterprise knowledge retrieval and agentic reasoning.

---

## 3. Product Vision

> Transform supply-chain data and operational knowledge into an intelligent,
> evidence-grounded decision-support system.

Aegis should enable users to move through four stages:

    MONITOR → INVESTIGATE → SIMULATE → DECIDE

The system should provide evidence and analytical context rather than
presenting unsupported AI-generated business decisions as facts.

Aegis is a decision-support system rather than an autonomous operational
control system.

---

## 4. Target Users

### 4.1 Supply Chain Analyst

Primary needs:

- Analyze operational metrics.
- Investigate anomalies.
- Compare suppliers.
- Analyze inventory.
- Query supply-chain data.
- Retrieve operational documentation.
- Create analytical visualizations.
- Explore trends and relationships.

### 4.2 Operations Manager

Primary needs:

- Understand operational disruptions.
- Identify potential root causes.
- Assess business impact.
- Explore hypothetical scenarios.
- Review operational risks.
- Understand trade-offs between potential actions.

### 4.3 Executive User

Primary needs:

- Understand overall supply-chain health.
- Identify major risks.
- Understand business impact.
- Review trends.
- Receive concise, evidence-backed explanations.
- Explore high-level scenarios.

---

# 5. Core Product Capabilities

## 5.1 Supply Chain Monitoring

Aegis will provide analytical visibility into:

- Supplier performance
- Inventory health
- Delivery performance
- Warehouse performance
- Logistics performance
- Supply-chain risk

Example metrics include:

- On-time delivery rate
- Average lead time
- Lead-time variability
- Inventory turnover
- Days of inventory
- Stockout risk
- Warehouse utilization
- Processing time
- Carrier performance
- Order fulfillment rate
- Return rate

---

## 5.2 AI Investigation

Users can ask questions such as:

> Why did on-time delivery fall this week?

> Which suppliers are contributing most to the deterioration?

> Which warehouses are experiencing bottlenecks?

> Why is this product at risk of stockout?

> Which carrier is responsible for most delivery delays?

The agent should:

1. Understand the question.
2. Identify relevant business entities.
3. Select appropriate tools.
4. Query structured data.
5. Retrieve relevant knowledge.
6. Analyze evidence.
7. Produce a grounded explanation.
8. Provide supporting evidence and sources.

---

## 5.3 Enterprise Knowledge Retrieval

Aegis will maintain a searchable knowledge base containing:

- Policies
- SOPs
- Supplier documents
- Contracts
- Incident reports
- Business definitions
- Operational documentation

The knowledge pipeline will include:

    Documents
        ↓
    Cleaning
        ↓
    Chunking
        ↓
    Metadata enrichment
        ↓
    Embeddings
        ↓
    Vector Search
        ↓
    Retrieval
        ↓
    Grounded generation

The retrieval system should support metadata associated with documents and
chunks, allowing retrieval to be refined using relevant attributes such as:

- Document type
- Supplier
- Warehouse
- Business domain
- Date
- Version
- Topic

---

## 5.4 Scenario Analysis

Users can explore hypothetical changes to the supply chain.

Initial scenarios include:

### Demand Increase

Example:

> What happens if electronics demand increases by 20%?

### Supplier Failure

Example:

> What happens if supplier S14 becomes unavailable?

### Warehouse Capacity Reduction

Example:

> What happens if warehouse W3 loses 25% capacity?

### Lead-Time Increase

Example:

> What happens if supplier lead times increase by 15%?

Scenario calculations should be performed by deterministic analytical
logic where possible.

The generative AI layer should explain the calculated results rather than
inventing them.

---

## 5.5 Evidence-Grounded Answers

Aegis should distinguish between:

- Observed data
- Calculated metrics
- Retrieved documentation
- AI-generated interpretation

Where possible, answers should expose supporting evidence.

Example:

    Finding:
    Supplier S14 appears to be contributing to delivery deterioration.

    Evidence:
    - Late delivery rate increased from 9.7% to 18.4%.
    - Average lead time increased from 2.1 to 3.8 days.
    - 63% of affected shipments are associated with S14.

    Supporting sources:
    - Supplier performance data
    - Delivery records
    - Supplier documentation

The system should avoid presenting unsupported AI-generated claims as
observed facts.

---

## 5.6 Conversational Analytics & Visualization

Aegis will support analytical visualizations as part of natural-language
responses.

Users should not be required to explicitly request a chart when a
visualization materially improves understanding of the requested analysis.

For example:

> Show me how on-time delivery changed over the last 12 weeks.

Aegis should be able to return:

1. The requested analytical result.
2. An appropriate visualization.
3. A concise interpretation.
4. Supporting data or evidence where appropriate.

### Initial Visualization Types

Aegis will initially support:

- Line charts
- Bar charts
- Stacked bar charts
- Scatter plots
- Simple composition charts
- Tables
- KPI cards

### Visualization Selection

The system should select an appropriate visualization based on analytical
intent and returned data.

Examples:

| Analytical question | Preferred visualization |
|---|---|
| Metric over time | Line chart |
| Supplier comparison | Bar chart |
| Top-N products | Bar chart |
| Category composition | Stacked bar / composition chart |
| Relationship between two metrics | Scatter plot |
| Monthly demand trend | Line chart |
| Warehouse comparison | Bar chart |
| Scenario comparison | Bar chart |
| Single important metric | KPI card |

The system should avoid generating a visualization when it does not add
meaningful value.

### Visualization Architecture

The LLM should not be responsible for inventing numerical values.

The visualization pipeline should follow:

    User Question
        ↓
    Agent / Intent Understanding
        ↓
    Analytical Query
        ↓
    SQL / Spark
        ↓
    Deterministic Result Set
        ↓
    Visualization Selection
        ↓
    Chart Specification
        ↓
    Application Rendering

The numerical values displayed in visualizations must originate from
deterministic analytical results.

The generative AI layer may determine the appropriate visualization type
and explain the results, but must not fabricate chart data.

### Conversational Analytics Examples

#### Example 1 — Trend

User:

> How has delivery performance changed over the last six months?

Expected response:

- Line chart showing delivery performance over time.
- Summary of the trend.
- Identification of significant changes.

#### Example 2 — Supplier Comparison

User:

> Compare our top ten suppliers by on-time delivery.

Expected response:

- Ranked bar chart.
- Supplier comparison.
- Identification of significant performance differences.

#### Example 3 — Relationship Analysis

User:

> Is supplier lead time related to late deliveries?

Expected response:

- Scatter plot.
- Statistical summary where appropriate.
- Explanation of the observed relationship.
- Explicit distinction between correlation and causation.

#### Example 4 — Inventory Risk

User:

> Which product categories have the highest stockout risk?

Expected response:

- Ranked bar chart.
- Stockout-risk metrics.
- Explanation of major contributing factors.

### Future Visualization Capabilities

Potential future capabilities include:

- Interactive filtering
- Drill-down analysis
- Cross-filtering between charts
- Scenario comparison visualizations
- Geographic visualizations
- Interactive dashboards

---

# 6. Data Domains

The initial synthetic AegisMart dataset will contain the following domains.

## 6.1 Customer

- customer_id
- region
- customer_segment

## 6.2 Product

- product_id
- category
- product_name
- unit_cost
- selling_price

## 6.3 Supplier

- supplier_id
- supplier_name
- region
- supplier_type

## 6.4 Supplier Product

- supplier_id
- product_id
- agreed_lead_time
- unit_cost
- minimum_order_quantity

## 6.5 Order

- order_id
- customer_id
- order_date
- region
- order_status

## 6.6 Order Item

- order_id
- product_id
- quantity
- unit_price

## 6.7 Warehouse

- warehouse_id
- region
- capacity
- warehouse_type

## 6.8 Inventory

- warehouse_id
- product_id
- inventory_date
- stock_quantity
- reserved_quantity

## 6.9 Shipment

- shipment_id
- order_id
- warehouse_id
- carrier_id
- shipment_date
- expected_delivery_date

## 6.10 Delivery

- shipment_id
- actual_delivery_date
- delivery_status

## 6.11 Carrier

- carrier_id
- carrier_name
- service_type

## 6.12 Returns

- return_id
- order_id
- product_id
- return_date
- return_reason

---

# 7. Synthetic Data Strategy

Aegis will use a synthetic supply-chain dataset.

The dataset will be designed to represent a realistic enterprise environment
while remaining fully reproducible.

The data generator will intentionally introduce controlled operational events
that can later be used for testing and evaluation.

Examples:

### Supplier Degradation

Supplier S14 experiences increasing lead times and late deliveries.

### Warehouse Bottleneck

Warehouse W3 experiences increased processing time.

### Demand Shock

Demand for a product category increases significantly.

### Carrier Degradation

Carrier C7 experiences increased transit times.

### Inventory Anomaly

Actual demand deviates significantly from expected demand.

These events will provide known ground truth for evaluating the AI
investigation system.

The data generator should make it possible to reproduce the same scenarios
across development and evaluation runs.

---

# 8. Data Architecture

Aegis will use a Medallion-style architecture.

## 8.1 Bronze

Raw ingested data.

Examples:

- bronze_orders
- bronze_order_items
- bronze_inventory
- bronze_suppliers
- bronze_shipments
- bronze_deliveries

Responsibilities:

- Preserve source data.
- Maintain ingestion metadata.
- Handle raw records.
- Provide reproducible ingestion.

---

## 8.2 Silver

Cleaned and standardized data.

Examples:

- silver_orders
- silver_order_items
- silver_inventory
- silver_suppliers
- silver_shipments
- silver_deliveries

Responsibilities:

- Data cleansing.
- Type standardization.
- Deduplication.
- Business-rule validation.
- Joining reference data.
- Handling missing values.
- Standardizing identifiers.

---

## 8.3 Gold

Business-ready analytical datasets.

Examples:

- gold_supplier_performance
- gold_inventory_health
- gold_delivery_performance
- gold_warehouse_performance
- gold_carrier_performance
- gold_supply_chain_risk

Responsibilities:

- Business metrics.
- Aggregations.
- Analytical features.
- Risk indicators.
- Dashboard-ready datasets.
- AI-consumable analytical datasets.

---

# 9. AI Architecture

The AI layer will consist of several components.

## 9.1 Retrieval

- Document processing
- Chunking
- Metadata enrichment
- Embeddings
- Vector search
- Metadata filtering
- Retrieval evaluation

## 9.2 Agent

The Aegis agent will have controlled tools including:

- Search knowledge
- Query supply-chain data
- Get supplier performance
- Get inventory risk
- Get delivery metrics
- Get warehouse metrics
- Get carrier metrics
- Get incident history
- Run scenario analysis
- Get business definitions

The agent should select tools based on the user's request.

---

# 10. Separation of Responsibilities

Aegis will follow a strict separation between deterministic computation
and generative reasoning.

## 10.1 Deterministic Systems

Spark / SQL / Python analytics should calculate:

- Metrics
- Aggregations
- Trends
- Risk indicators
- Scenario outputs
- Statistical comparisons
- Ranking
- Time-series values

## 10.2 Generative AI

The AI layer should perform:

- Intent interpretation
- Tool selection
- Knowledge retrieval
- Evidence synthesis
- Natural-language explanation
- Conversational interaction
- Visualization selection

The LLM should not be relied upon for calculations that can be performed
deterministically.

---

# 11. Root Cause Investigation

Root-cause investigation is a core Aegis capability.

Example:

> Why did on-time delivery decline?

The system should investigate:

1. Overall performance change.
2. Affected regions.
3. Affected warehouses.
4. Affected suppliers.
5. Affected carriers.
6. Historical trends.
7. Data-quality anomalies.
8. Relevant incidents.
9. Relevant policies or SOPs.
10. Supporting evidence.

The final response should distinguish:

- Observed facts
- Calculated evidence
- Possible contributing factors
- Retrieved documentation
- AI interpretation

The system should avoid presenting a hypothesis as a confirmed root cause
unless sufficient evidence exists.

---

# 12. Scenario Engine

The scenario engine will perform deterministic calculations where possible.

Example:

    Demand +20%
          ↓
    Projected demand
          ↓
    Inventory consumption
          ↓
    Stockout analysis
          ↓
    Supplier capacity
          ↓
    Warehouse capacity
          ↓
    Service-level impact

The AI layer will explain the scenario output and surface important
trade-offs.

Scenario results should identify assumptions used in the calculation.

For example:

- Demand growth assumption
- Forecast period
- Lead-time assumption
- Available inventory
- Supplier capacity
- Warehouse capacity

---

# 13. Evaluation

Aegis will contain a dedicated evaluation framework.

The evaluation dataset will include:

- User questions
- Expected tools
- Expected entities
- Expected sources
- Expected answers
- Difficulty
- Ground-truth incident
- Expected analytical result where applicable

The system will evaluate:

## 13.1 Retrieval

Did the system retrieve relevant information?

## 13.2 Tool Selection

Did the agent select appropriate tools?

## 13.3 SQL Correctness

Was the generated analytical query correct?

## 13.4 Analytical Correctness

Did the system calculate the correct metric or result?

## 13.5 Groundedness

Is the response supported by retrieved evidence?

## 13.6 Answer Quality

Does the response address the user's question?

## 13.7 Citation Quality

Do cited sources support the claims?

## 13.8 Visualization Correctness

Did the system:

- Select an appropriate chart type?
- Use the correct analytical result?
- Preserve the correct values?
- Avoid misleading visualizations?

## 13.9 Safety

Does the agent respect defined access and execution constraints?

---

# 14. Observability

Aegis should track AI interactions including:

- Request ID
- User question
- Agent version
- Prompt version
- Tools called
- Retrieved documents
- Query execution
- Visualization type
- Response latency
- Errors
- User feedback
- Evaluation results

The system should support analysis of:

- Latency
- Failure rate
- Retrieval quality
- Groundedness
- Tool usage
- Query performance
- Visualization usage
- User feedback
- Evaluation scores

---

# 15. Governance

Aegis will use Databricks-native governance capabilities where available.

The system should consider:

- Data access
- Table organization
- Data lineage
- AI interaction logging
- Safe SQL execution
- Prompt controls
- Sensitive data handling
- Auditability
- Agent tool permissions

The system should follow the principle of least privilege for tools and
data access.

---

# 16. Application

The final Aegis application should contain the following major areas.

## 16.1 Executive Dashboard

High-level supply-chain health.

Potential metrics:

- On-time delivery
- Inventory risk
- Supplier risk
- Warehouse utilization
- Open incidents

---

## 16.2 AI Analyst

Natural-language interaction with the supply chain.

Capabilities:

- Natural-language questions
- Structured data queries
- Knowledge retrieval
- Charts
- Tables
- Evidence
- Follow-up questions

---

## 16.3 Investigations

AI-assisted root-cause investigations.

Capabilities:

- Investigation creation
- Evidence collection
- Timeline
- Affected entities
- Hypotheses
- Supporting metrics
- Relevant documents
- Investigation summary

---

## 16.4 Scenario Planning

What-if analysis.

Capabilities:

- Demand scenarios
- Supplier failure scenarios
- Warehouse capacity scenarios
- Lead-time scenarios
- Scenario comparison
- Business impact analysis

---

## 16.5 Suppliers

Supplier performance and risk.

Capabilities:

- Supplier scorecards
- Delivery performance
- Lead time
- Defect rate
- Historical trends
- Risk indicators
- Related incidents
- Supplier documentation

---

## 16.6 Inventory

Inventory health and stockout risk.

Capabilities:

- Inventory levels
- Days of inventory
- Stockout risk
- Demand trends
- Replenishment indicators
- Product/category analysis

---

## 16.7 Warehouses

Warehouse performance.

Capabilities:

- Throughput
- Utilization
- Processing time
- Backlog
- Delivery impact
- Historical performance

---

## 16.8 Logistics

Shipment and delivery performance.

Capabilities:

- Carrier performance
- Transit time
- On-time delivery
- Delayed shipments
- Route/region analysis

---

## 16.9 Knowledge Center

Enterprise knowledge retrieval.

Capabilities:

- Search
- Document filtering
- Source inspection
- Policy lookup
- Incident lookup
- Business glossary

---

## 16.10 Monitoring

Data and AI system monitoring.

Capabilities:

- Pipeline health
- Data quality
- Agent latency
- Tool failures
- Retrieval performance
- Evaluation metrics
- User feedback

---

# 17. Design Principles

Aegis will follow these principles.

## 17.1 Evidence Over Hallucination

AI responses should be grounded in data or retrieved knowledge.

---

## 17.2 Deterministic Computation Over LLM Calculation

Use SQL, Spark, and Python for calculations whenever possible.

---

## 17.3 Explainability

Important conclusions should expose supporting evidence.

---

## 17.4 Reproducibility

Data generation, transformations, evaluation and experiments should be
reproducible.

---

## 17.5 Minimal Complexity

Technology should be introduced because it solves a problem, not because
it makes the architecture look impressive.

---

## 17.6 Production-Oriented Engineering

The system should include:

- Testing
- Version control
- Monitoring
- Evaluation
- Error handling
- Documentation
- Reproducible workflows

---

## 17.7 Free Edition Compatibility

The implementation must remain compatible with Databricks Free Edition
constraints.

Where Free Edition limitations prevent true production deployment,
the project should document the limitation and maintain a production-oriented
architecture.

---

## 17.8 Human Decision Support

Aegis should support human decision-making rather than autonomously making
high-impact operational decisions.

The system should present:

- Evidence
- Assumptions
- Calculated impacts
- Potential options
- Trade-offs

rather than presenting AI-generated recommendations as unquestionable
decisions.

---

# 18. Definition of Done

Aegis v1.0 is considered complete when a user can:

1. View supply-chain health.
2. Explore supplier, inventory, warehouse and delivery metrics.
3. Ask natural-language questions.
4. Receive answers grounded in structured data.
5. Retrieve enterprise documentation.
6. Investigate supply-chain anomalies.
7. Receive evidence-backed root-cause analysis.
8. Run predefined business scenarios.
9. Understand scenario impacts.
10. View supporting evidence.
11. Receive appropriate visualizations for analytical queries.
12. Inspect the underlying evidence/data supporting visualizations.
13. Provide feedback.
14. Evaluate AI responses.
15. View system and AI monitoring information.

The complete system should be documented and reproducible from the public
GitHub repository.

---

# 19. Project Success Criteria

The project should demonstrate competence across:

- Data engineering
- Delta Lake
- Spark
- SQL
- Data modeling
- Data quality
- Supply-chain analytics
- Retrieval-augmented generation
- Embeddings
- Vector search
- Agentic AI
- Tool calling
- Prompt engineering
- Conversational analytics
- Data visualization
- Scenario analysis
- Evaluation
- MLflow
- Governance
- Monitoring
- Application development

The project should prioritize depth and engineering quality over the number
of technologies used.

---

# 20. Current Scope

## In Scope

- Synthetic supply-chain data
- Medallion architecture
- Supply-chain analytics
- Enterprise knowledge base
- RAG
- AI agent
- Tool calling
- Root-cause investigation
- Scenario analysis
- Conversational analytics
- Data visualization
- Evaluation
- Monitoring
- Governance
- Databricks application

## Out of Scope for v1

- Autonomous purchasing
- Autonomous supplier communication
- Autonomous inventory orders
- Real-world ERP integration
- Financial transactions
- Fully autonomous business decisions

Aegis is a decision-support system, not an autonomous operational control
system.

---


**Next Phase:** Phase 1 — Architecture & Data Model