from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


DOCUMENT_COLUMNS = {
    "document_type": "VARCHAR(64)",
    "classification_confidence": "FLOAT",
    "detected_language": "VARCHAR(16)",
    "original_text": "TEXT",
    "translated_text": "TEXT",
    "extracted_data": "JSON",
    "processing_error": "TEXT",
}


def ensure_schema(engine: Engine) -> None:
    """Add Phase 2 columns to existing Phase 1 tables without dropping data."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if "documents" not in tables:
        return
    existing = {column["name"] for column in inspector.get_columns("documents")}
    dialect = engine.dialect.name
    with engine.begin() as connection:
        for name, sql_type in DOCUMENT_COLUMNS.items():
            if name in existing:
                continue
            column_type = "TEXT" if dialect == "sqlite" and sql_type == "JSON" else sql_type
            connection.execute(text(f"ALTER TABLE documents ADD COLUMN {name} {column_type}"))
