from unitycatalog.ai.core.databricks import DatabricksFunctionClient

client = DatabricksFunctionClient()

result = client.execute_function(
    function_name="workspace.aegis_gold.get_supplier_performance",
    parameters={
        "p_supplier_id": "SUP0014",
        "p_start_date": "2025-01-01",
        "p_end_date": "2025-04-30",
    },
)

print(result.value)