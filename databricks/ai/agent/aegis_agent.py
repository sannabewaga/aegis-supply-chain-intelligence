import json
from databricks.ai.rag.documents.retrieve import search_knowledge
from google import genai
from unitycatalog.ai.core.databricks import DatabricksFunctionClient

print("1. Imports complete")

# ============================================================
# 1. CONFIGURATION
# ============================================================

MODEL = "gemini-3.5-flash-lite"

MAX_STEPS = 6

SECRET_SCOPE = "aegis-secrets"
SECRET_KEY = "gemini-api-key"

print("2. Secret retrieved")

# ============================================================
# 2. GEMINI CLIENT
# ============================================================

api_key = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key=SECRET_KEY,
)

gemini = genai.Client(
    api_key=api_key
)

print("3. Gemini client created")

# ============================================================
# 3. UNITY CATALOG CLIENT
# ============================================================

uc_client = DatabricksFunctionClient()

print("4. UC client created")

print("5. Ready to run agent")
# ============================================================
# 4. TOOL DEFINITIONS
# ============================================================

TOOLS = [
    {
    "type": "function",
    "name": "get_supplier_network",
    "description": (
        "Discover the warehouses and carriers actually handling "
        "a supplier's shipments during a specified period. "
        "Use this before investigating whether a warehouse or "
        "carrier contributed to a supplier performance problem."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "supplier_id": {
                "type": "string",
                "description": "Supplier ID such as SUP0014.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date in YYYY-MM-DD format.",
            },
            "end_date": {
                "type": "string",
                "description": "End date in YYYY-MM-DD format.",
            },
        },
        "required": [
            "supplier_id",
            "start_date",
            "end_date",
        ],
    },
},
    {
        "type": "function",
        "name": "search_enterprise_knowledge",
        "description": (
            "Search Aegis's enterprise knowledge base for "
            "policies, metric definitions, operational rules, "
            "SLA thresholds, escalation guidance, and other "
            "documented business knowledge. Use this when "
            "answering questions that require company policy "
            "or definitions rather than raw operational metrics."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A focused natural-language question "
                        "to search the enterprise knowledge base."
                    ),
                },
            },
            "required": ["query"],
        },
    },
    {
        "type": "function",
        "name": "get_supplier_performance",
        "description": (
            "Retrieve monthly supplier performance metrics "
            "for a specific supplier and date range. Use for "
            "supplier delivery reliability, late delivery "
            "rate, shipments, revenue, units supplied, and "
            "supplier trends."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "supplier_id": {
                    "type": "string",
                    "description": (
                        "Supplier ID such as SUP0014."
                    ),
                },
                "start_date": {
                    "type": "string",
                    "description": (
                        "Start date in YYYY-MM-DD format."
                    ),
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "End date in YYYY-MM-DD format."
                    ),
                },
            },
            "required": [
                "supplier_id",
                "start_date",
                "end_date",
            ],
        },
    },

    {
        "type": "function",
        "name": "get_delivery_performance",
        "description": (
            "Retrieve monthly delivery performance for a "
            "warehouse, carrier, or both. Use for shipment "
            "volume, late shipments, late delivery rate, "
            "transit time, and delivery delays."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "warehouse_id": {
                    "type": "string",
                    "description": (
                        "Warehouse ID such as WH0003."
                    ),
                },
                "carrier_id": {
                    "type": "string",
                    "description": (
                        "Carrier ID such as CAR0007."
                    ),
                },
                "start_date": {
                    "type": "string",
                    "description": (
                        "Start date in YYYY-MM-DD format."
                    ),
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "End date in YYYY-MM-DD format."
                    ),
                },
            },
            "required": [
                "start_date",
                "end_date",
            ],
        },
    },

    {
        "type": "function",
        "name": "get_inventory_health",
        "description": (
            "Retrieve daily inventory health for a warehouse "
            "and/or product over a date range. Use for stock "
            "levels, available inventory, stockouts, and "
            "inventory-demand ratios."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "warehouse_id": {
                    "type": "string",
                    "description": (
                        "Warehouse ID such as WH0003."
                    ),
                },
                "product_id": {
                    "type": "string",
                    "description": (
                        "Product ID such as PRD0001."
                    ),
                },
                "start_date": {
                    "type": "string",
                    "description": (
                        "Start date in YYYY-MM-DD format."
                    ),
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "End date in YYYY-MM-DD format."
                    ),
                },
            },
            "required": [
                "start_date",
                "end_date",
            ],
        },
    },

    {
        "type": "function",
        "name": "get_warehouse_performance",
        "description": (
            "Retrieve monthly warehouse performance metrics "
            "for a specific warehouse. Use for throughput, "
            "late delivery rate, delivery delay, inventory "
            "health, and stockout rate."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "warehouse_id": {
                    "type": "string",
                    "description": (
                        "Warehouse ID such as WH0003."
                    ),
                },
                "start_date": {
                    "type": "string",
                    "description": (
                        "Start date in YYYY-MM-DD format."
                    ),
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "End date in YYYY-MM-DD format."
                    ),
                },
            },
            "required": [
                "warehouse_id",
                "start_date",
                "end_date",
            ],
        },
    },

    {
        "type": "function",
        "name": "get_carrier_performance",
        "description": (
            "Retrieve monthly carrier performance metrics "
            "for a specific carrier. Use for delivery "
            "reliability, transit time, delay, variability, "
            "and late delivery rate."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "carrier_id": {
                    "type": "string",
                    "description": (
                        "Carrier ID such as CAR0007."
                    ),
                },
                "start_date": {
                    "type": "string",
                    "description": (
                        "Start date in YYYY-MM-DD format."
                    ),
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "End date in YYYY-MM-DD format."
                    ),
                },
            },
            "required": [
                "carrier_id",
                "start_date",
                "end_date",
            ],
        },
    },

    {
        "type": "function",
        "name": "get_supply_chain_risk",
        "description": (
            "Retrieve deterministic supply-chain risk signals "
            "for a supplier over a date range. Use for supplier "
            "risk, operational risk, and potential disruption "
            "signals."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "supplier_id": {
                    "type": "string",
                    "description": (
                        "Supplier ID such as SUP0014."
                    ),
                },
                "start_date": {
                    "type": "string",
                    "description": (
                        "Start date in YYYY-MM-DD format."
                    ),
                },
                "end_date": {
                    "type": "string",
                    "description": (
                        "End date in YYYY-MM-DD format."
                    ),
                },
            },
            "required": [
                "supplier_id",
                "start_date",
                "end_date",
            ],
        },
    },
]


# ============================================================
# 5. GEMINI TOOL → UNITY CATALOG FUNCTION
# ============================================================

FUNCTION_MAP = {

    "get_supplier_network":
    "workspace.aegis_gold.get_supplier_network",

    "get_supplier_performance":
        "workspace.aegis_gold.get_supplier_performance",

    "get_delivery_performance":
        "workspace.aegis_gold.get_delivery_performance",

    "get_inventory_health":
        "workspace.aegis_gold.get_inventory_health",

    "get_warehouse_performance":
        "workspace.aegis_gold.get_warehouse_performance",

    "get_carrier_performance":
        "workspace.aegis_gold.get_carrier_performance",

    "get_supply_chain_risk":
        "workspace.aegis_gold.get_supply_chain_risk",
}


# ============================================================
# 6. GEMINI PARAMETER → UC PARAMETER MAPPING
# ============================================================

PARAMETER_MAP = {

    "get_supplier_network": {
    "supplier_id": "p_supplier_id",
    "start_date": "p_start_date",
    "end_date": "p_end_date",
    },

    "get_supplier_performance": {
        "supplier_id": "p_supplier_id",
        "start_date": "p_start_date",
        "end_date": "p_end_date",
    },

    "get_delivery_performance": {
        "warehouse_id": "p_warehouse_id",
        "carrier_id": "p_carrier_id",
        "start_date": "p_start_date",
        "end_date": "p_end_date",
    },

    "get_inventory_health": {
        "warehouse_id": "p_warehouse_id",
        "product_id": "p_product_id",
        "start_date": "p_start_date",
        "end_date": "p_end_date",
    },

    "get_warehouse_performance": {
        "warehouse_id": "p_warehouse_id",
        "start_date": "p_start_date",
        "end_date": "p_end_date",
    },

    "get_carrier_performance": {
        "carrier_id": "p_carrier_id",
        "start_date": "p_start_date",
        "end_date": "p_end_date",
    },

    "get_supply_chain_risk": {
        "supplier_id": "p_supplier_id",
        "start_date": "p_start_date",
        "end_date": "p_end_date",
    },
}


# ============================================================
# 7. EXECUTE UNITY CATALOG TOOL
# ============================================================

def execute_tool(
    function_name: str,
    arguments: dict,
):
    if function_name == "search_enterprise_knowledge":
        query = arguments["query"]
        return search_knowledge(
            query=query,
            num_results=5,
        )

    if function_name not in FUNCTION_MAP:
        raise ValueError(
            f"Unknown Aegis tool: {function_name}"
        )

    uc_function = FUNCTION_MAP[function_name]
    parameter_mapping = PARAMETER_MAP[function_name]
    uc_parameters = {}

    for gemini_parameter, value in arguments.items():
        if gemini_parameter not in parameter_mapping:
            raise ValueError(
                f"Unexpected parameter "
                f"'{gemini_parameter}' "
                f"for tool '{function_name}'"
            )

        uc_parameter = parameter_mapping[gemini_parameter]
        uc_parameters[uc_parameter] = value

        # get_delivery_performance accepts optional warehouse/carrier filters.
    # Unity Catalog still requires values for all function parameters,
    # so explicitly pass NULL when the agent does not specify them.

    if function_name == "get_delivery_performance":
        uc_parameters.setdefault("p_warehouse_id", None)
        uc_parameters.setdefault("p_carrier_id", None)
    result = uc_client.execute_function(
        function_name=uc_function,
        parameters=uc_parameters,
    )

    return result.value


# ============================================================
# 8. AEGIS AGENT LOOP
# ============================================================

def ask_aegis(question: str):

    print("\n" + "=" * 70)
    print("AEGIS AGENT")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1: Give the user question to Gemini
    # --------------------------------------------------------

    interaction = gemini.interactions.create(
        model=MODEL,
        input=question,
        tools=TOOLS,
        system_instruction=(
            "You are Aegis, an enterprise supply-chain "
            "intelligence agent.\n\n"

            "Use analytical tools whenever factual business "
            "metrics are required.\n\n"

            "Use search_enterprise_knowledge when you need "
            "company policies, SLA thresholds, metric definitions, "
            "operational rules, or escalation guidance.\n\n"

            "You may use multiple tools and combine their evidence "
            "before answering.\n\n"

            "Never invent numeric business metrics.\n\n"

            "Distinguish observed facts, documented policy, "
            "correlation, plausible explanations, and confirmed "
            "evidence.\n\n"

            "Do not claim causation unless the available evidence "
            "supports it."
            "Use get_supplier_network when investigating "
            "relationships between suppliers, warehouses, and carriers. "
            "Use the discovered warehouse and carrier IDs to drill into "
            "their performance with the appropriate analytical tools.\n\n"
        ),
    )

    # --------------------------------------------------------
    # AGENT LOOP
    # --------------------------------------------------------

    for step_number in range(1, MAX_STEPS + 1):

        print(
            f"\n--- Agent step "
            f"{step_number}/{MAX_STEPS} ---"
        )

        # ----------------------------------------------------
        # Find all tool calls in this interaction
        # ----------------------------------------------------

        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        # ----------------------------------------------------
        # No tool call = Gemini has produced final answer
        # ----------------------------------------------------

        if not function_calls:

            print("\nAgent finished.")

            return interaction.output_text

        # ----------------------------------------------------
        # Execute every requested tool
        # ----------------------------------------------------

        function_results = []

        for function_call in function_calls:

            function_name = function_call.name
            arguments = function_call.arguments

            print(
                f"\nTool requested: {function_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            result = execute_tool(
                function_name=function_name,
                arguments=arguments,
            )

            print(
                f"Tool completed: {function_name}"
            )

            function_results.append(
                {
                    "type": "function_result",
                    "name": function_name,
                    "call_id": function_call.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                result,
                                default=str,
                            ),
                        }
                    ],
                }
            )

        # ----------------------------------------------------
        # Send ALL tool results back to the SAME interaction
        # ----------------------------------------------------

        interaction = gemini.interactions.create(
            model=MODEL,
            previous_interaction_id=interaction.id,
            tools=TOOLS,
            input=function_results,
        )

    # --------------------------------------------------------
    # Safety limit
    # --------------------------------------------------------

    return (
        "I reached the maximum number of analytical steps "
        "allowed for this request. Please narrow the question "
        "or specify the supplier, warehouse, carrier, "
        "or product you want me to investigate."
    )

# ============================================================
# 9. TEST
# ============================================================

if __name__ == "__main__":

    question = (
        "Investigate why supplier SUP0014 experienced a major deterioration in February 2025. Determine whether the evidence points primarily to a supplier issue, warehouse issue, or carrier issue. Compare the supplier's February performance against its January performance, investigate the relevant warehouse and carrier performance, check the documented company policies and escalation guidance, and explain what evidence supports or contradicts each possible root cause. Do not claim causation unless the data supports it."
    )

    answer = ask_aegis(question)

    print("\n")
    print("=" * 70)
    print("FINAL AEGIS RESPONSE")
    print("=" * 70)
    print(answer)