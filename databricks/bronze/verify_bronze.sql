SELECT
    'customer' AS table_name,
    COUNT(*) AS row_count
FROM workspace.aegis_bronze.customer

UNION ALL
SELECT 'product', COUNT(*)
FROM workspace.aegis_bronze.product

UNION ALL
SELECT 'supplier', COUNT(*)
FROM workspace.aegis_bronze.supplier

UNION ALL
SELECT 'supplier_product', COUNT(*)
FROM workspace.aegis_bronze.supplier_product

UNION ALL
SELECT 'warehouse', COUNT(*)
FROM workspace.aegis_bronze.warehouse

UNION ALL
SELECT 'carrier', COUNT(*)
FROM workspace.aegis_bronze.carrier

UNION ALL
SELECT 'order', COUNT(*)
FROM workspace.aegis_bronze.order

UNION ALL
SELECT 'order_item', COUNT(*)
FROM workspace.aegis_bronze.order_item

UNION ALL
SELECT 'shipment', COUNT(*)
FROM workspace.aegis_bronze.shipment

UNION ALL
SELECT 'shipment_item', COUNT(*)
FROM workspace.aegis_bronze.shipment_item

UNION ALL
SELECT 'inventory_snapshot', COUNT(*)
FROM workspace.aegis_bronze.inventory_snapshot

UNION ALL
SELECT 'return', COUNT(*)
FROM workspace.aegis_bronze.return

UNION ALL
SELECT 'ground_truth_incidents', COUNT(*)
FROM workspace.aegis_bronze.ground_truth_incidents;