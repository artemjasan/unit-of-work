from dataclasses import dataclass, field
import os


@dataclass(slots=True)
class AppConfig:
    db_url: str = field(default_factory=lambda: os.getenv("DB_URL", "sql/blog.db"))
    db_schema: str = field(
        default_factory=lambda: os.getenv("DB_SCHEMA", "sql/schema.sql")
    )
