from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

from app.constants import DEFAULT_SIGNUP_ROLE


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
    """Add newer columns to existing tables without dropping data."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    dialect = engine.dialect.name
    with engine.begin() as connection:
        if "documents" in tables:
            existing = {column["name"] for column in inspector.get_columns("documents")}
            for name, sql_type in DOCUMENT_COLUMNS.items():
                if name in existing:
                    continue
                column_type = "TEXT" if dialect == "sqlite" and sql_type == "JSON" else sql_type
                connection.execute(text(f"ALTER TABLE documents ADD COLUMN {name} {column_type}"))

        if "users" in tables:
            user_cols = {column["name"] for column in inspector.get_columns("users")}
            if "role" not in user_cols:
                default = DEFAULT_SIGNUP_ROLE.replace("'", "''")
                if dialect == "sqlite":
                    connection.execute(text(f"ALTER TABLE users ADD COLUMN role VARCHAR(32) DEFAULT '{default}'"))
                else:
                    connection.execute(
                        text(f"ALTER TABLE users ADD COLUMN role VARCHAR(32) NOT NULL DEFAULT '{default}'")
                    )
                    connection.execute(text("CREATE INDEX IF NOT EXISTS ix_users_role ON users (role)"))
