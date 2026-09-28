from retrieve import search_knowledge, format_context


query = "What is the expected on-time delivery performance for suppliers?"

evidence = search_knowledge(
    query,
    num_results=3
)

context = format_context(evidence)

print(context)