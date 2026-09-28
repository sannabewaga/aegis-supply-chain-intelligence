# ============================================================
# AEGIS — RAG DOCUMENT INGESTION
# ============================================================

from pathlib import Path
import re
import pandas as pd

# ------------------------------------------------------------
# 1. Locate the documents directory
# ------------------------------------------------------------

cwd = Path.cwd()

print("Current working directory:")
print(cwd)

# Search upward for our documents directory
document_candidates = list(cwd.parents) + [cwd]

documents_dir = None

for path in document_candidates:
    candidate = path / "databricks" / "ai" / "rag" / "documents"

    if candidate.exists():
        documents_dir = candidate
        break

if documents_dir is None:
    raise FileNotFoundError(
        "Could not find databricks/ai/rag/documents "
        "from the current Git folder."
    )

print(f"\nDocuments directory: {documents_dir}")


# ------------------------------------------------------------
# 2. Load Markdown files
# ------------------------------------------------------------

files = sorted(documents_dir.glob("*.md"))

print(f"\nFound {len(files)} documents:")

for file in files:
    print(f" - {file.name}")

if len(files) != 7:
    raise ValueError(
        f"Expected 7 Markdown documents, found {len(files)}."
    )


# ------------------------------------------------------------
# 3. Chunk documents
# ------------------------------------------------------------

def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_markdown(text: str, max_chars: int = 1400):
    """
    Split Markdown into meaningful chunks.

    Headings are treated as context rather than standalone chunks.
    Small sections are merged with their following content.
    """

    text = clean_text(text)

    # Split into Markdown sections while retaining the heading
    sections = re.split(
        r"(?=^#{1,3}\s+)",
        text,
        flags=re.MULTILINE
    )

    sections = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    chunks = []

    for section in sections:

        # Ignore completely standalone headings
        lines = section.splitlines()

        non_heading_lines = [
            line.strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]

        if not non_heading_lines:
            continue

        # Small enough → keep the entire section together
        if len(section) <= max_chars:
            chunks.append(section)
            continue

        # Large section:
        # split by paragraphs while preserving the heading
        heading_match = re.match(
            r"^(#{1,3}\s+.+?)(?:\n|$)",
            section
        )

        heading = (
            heading_match.group(1)
            if heading_match
            else ""
        )

        body = (
            section[heading_match.end():].strip()
            if heading_match
            else section
        )

        paragraphs = body.split("\n\n")

        current = heading

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            candidate = (
                f"{current}\n\n{paragraph}"
                if current
                else paragraph
            )

            if len(candidate) <= max_chars:
                current = candidate

            else:
                if current and current != heading:
                    chunks.append(current)

                current = (
                    f"{heading}\n\n{paragraph}"
                    if heading
                    else paragraph
                )

        if current and current != heading:
            chunks.append(current)

    return chunks

# ------------------------------------------------------------
# 4. Build chunk records
# ------------------------------------------------------------

records = []

for file in files:

    document_name = file.stem
    document_type = "policy"

    text = file.read_text(encoding="utf-8")

    chunks = chunk_markdown(text)

    for chunk_number, chunk in enumerate(chunks):

        # Extract first Markdown heading if available
        heading_match = re.search(
            r"^#{1,3}\s+(.+)$",
            chunk,
            flags=re.MULTILINE
        )

        section = (
            heading_match.group(1).strip()
            if heading_match
            else "General"
        )

        chunk_id = (
            f"{document_name}_"
            f"{chunk_number:03d}"
        )

        records.append({
            "chunk_id": chunk_id,
            "document_name": document_name,
            "document_type": document_type,
            "section": section,
            "chunk_number": chunk_number,
            "text": chunk
        })


print(f"\nCreated {len(records)} chunks.")


# ------------------------------------------------------------
# 5. Create Spark DataFrame
# ------------------------------------------------------------

chunks_df = spark.createDataFrame(
    pd.DataFrame(records)
)


# ------------------------------------------------------------
# 6. Write Delta table
# ------------------------------------------------------------

target_table = "workspace.aegis_ai.document_chunks"

(
    chunks_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(target_table)
)

print(f"\nWritten to: {target_table}")


# ------------------------------------------------------------
# 7. Verification
# ------------------------------------------------------------

display(
    spark.sql(f"""
        SELECT
            document_name,
            COUNT(*) AS chunk_count
        FROM {target_table}
        GROUP BY document_name
        ORDER BY document_name
    """)
)