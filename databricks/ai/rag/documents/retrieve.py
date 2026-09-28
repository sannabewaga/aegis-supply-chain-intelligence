from databricks.ai_search.client import AISearchClient


AI_SEARCH_ENDPOINT = "enterprise-ai-search"
INDEX_NAME = "workspace.aegis_ai.aegis_index"

client = AISearchClient()

index = client.get_index(
    endpoint_name=AI_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
)


def search_knowledge(query: str, num_results: int = 5):
    """Search the Aegis enterprise knowledge base."""

    results = index.similarity_search(
        query_text=query,
        columns=[
            "text",
            "chunk_id",
            "document_name",
            "document_type",
            "section",
        ],
        num_results=num_results,
        query_type="hybrid",
    )

    evidence = []

    columns = [
        column["name"]
        for column in results["manifest"]["columns"]
    ]

    for row in results["result"]["data_array"]:
        row_data = dict(zip(columns, row))

        evidence.append({
            "text": row_data.get("text"),
            "chunk_id": row_data.get("chunk_id"),
            "document_name": row_data.get("document_name"),
            "document_type": row_data.get("document_type"),
            "section": row_data.get("section"),
            "score": row_data.get("score"),
        })

    return evidence


def format_context(evidence):
    """
    Convert retrieved knowledge chunks into clean,
    source-attributed context for the LLM.
    """

    if not evidence:
        return "No relevant enterprise knowledge was retrieved."

    sections = []

    for i, item in enumerate(evidence, start=1):
        section = f"""SOURCE {i}
Document: {item["document_name"]}
Section: {item["section"]}
Chunk ID: {item["chunk_id"]}
Relevance Score: {item["score"]:.3f}

{item["text"]}
"""

        sections.append(section)

    return "\n\n---\n\n".join(sections)