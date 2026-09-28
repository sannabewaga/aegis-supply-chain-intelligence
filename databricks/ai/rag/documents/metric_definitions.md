# AegisMart Metric Definitions

## Supplier Metrics

### Late Delivery Rate

Late Delivery Rate = Late Shipments / Total Shipments

A shipment is late when its actual delivery date exceeds its expected delivery date.

### Average Delivery Delay

Average Delivery Delay represents the average number of days by which deliveries exceed their expected delivery date.

### Average Actual Transit Days

Average Actual Transit Days represents the average duration between shipment date and actual delivery date.

## Inventory Metrics

### Available Quantity

Available Quantity = Stock Quantity - Reserved Quantity

### Stockout

A stockout occurs when Available Quantity is less than or equal to zero.

### Stockout Rate

Stockout Rate represents the proportion of inventory observations where a stockout condition is present.

## Warehouse Metrics

### Shipment Count

The number of shipments processed by a warehouse during the reporting period.

### Processing Efficiency

Processing Efficiency is the operational efficiency attribute associated with the warehouse.

It should be interpreted as a warehouse characteristic rather than independently treated as proof of a bottleneck.

## Carrier Metrics

### Transit Time Variability

Transit Time Variability represents the variability associated with carrier transit performance.

### Transit-Time Standard Deviation

Transit-Time Standard Deviation measures observed variation in actual transit times within the reporting period.

## Risk Metrics

### Risk Signal Score

Risk Signal Score is a deterministic composite of multiple operational warning signals.

It combines:

- Delivery risk.
- Delay risk.
- Inventory risk.
- Supplier reliability risk.

The score is a screening signal and is not a probability of failure.

## Analytical Principles

Metrics should always be interpreted in their relevant time period and operational context.

Comparisons should distinguish:

- Current performance.
- Historical performance.
- Peer performance.

A metric should not be interpreted as causal evidence unless additional evidence supports the conclusion.