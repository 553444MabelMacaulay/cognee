"""Configuration management for cognee.

This module handles loading and validating configuration settings
from environment variables and .env files.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


@dataclass
class LLMConfig:
    """Configuration for Large Language Model providers."""

    provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"))
    api_base: Optional[str] = field(default_factory=lambda: os.getenv("LLM_API_BASE"))
    temperature: float = field(default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.0")))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "4096")))


@dataclass
class VectorDBConfig:
    """Configuration for vector database backend."""

    provider: str = field(default_factory=lambda: os.getenv("VECTOR_DB_PROVIDER", "lancedb"))
    url: Optional[str] = field(default_factory=lambda: os.getenv("VECTOR_DB_URL"))
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("VECTOR_DB_API_KEY"))
    path: str = field(default_factory=lambda: os.getenv("VECTOR_DB_PATH", ".cognee_data/vector"))


@dataclass
class GraphDBConfig:
    """Configuration for graph database backend."""

    provider: str = field(default_factory=lambda: os.getenv("GRAPH_DB_PROVIDER", "networkx"))
    url: Optional[str] = field(default_factory=lambda: os.getenv("GRAPH_DB_URL"))
    username: Optional[str] = field(default_factory=lambda: os.getenv("GRAPH_DB_USERNAME"))
    password: Optional[str] = field(default_factory=lambda: os.getenv("GRAPH_DB_PASSWORD"))
    path: str = field(default_factory=lambda: os.getenv("GRAPH_DB_PATH", ".cognee_data/graph"))


@dataclass
class RelationalDBConfig:
    """Configuration for relational database backend."""

    provider: str = field(default_factory=lambda: os.getenv("DB_PROVIDER", "sqlite"))
    host: Optional[str] = field(default_factory=lambda: os.getenv("DB_HOST"))
    port: Optional[int] = field(
        default_factory=lambda: int(os.getenv("DB_PORT", "5432")) if os.getenv("DB_PORT") else None
    )
    name: str = field(default_factory=lambda: os.getenv("DB_NAME", "cognee"))
    username: Optional[str] = field(default_factory=lambda: os.getenv("DB_USERNAME"))
    password: Optional[str] = field(default_factory=lambda: os.getenv("DB_PASSWORD"))
    path: str = field(default_factory=lambda: os.getenv("DB_PATH", ".cognee_data/relational"))


@dataclass
class CogneeConfig:
    """Top-level configuration for the cognee system."""

    # Data storage root
    data_root_dir: str = field(
        default_factory=lambda: os.getenv("DATA_ROOT_DIR", str(Path.home() / ".cognee_data"))
    )

    # Sub-configs
    llm: LLMConfig = field(default_factory=LLMConfig)
    vector_db: VectorDBConfig = field(default_factory=VectorDBConfig)
    graph_db: GraphDBConfig = field(default_factory=GraphDBConfig)
    relational_db: RelationalDBConfig = field(default_factory=RelationalDBConfig)

    # Embedding model
    embedding_model: str = field(
        default_factory=lambda: os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    )
    embedding_dimensions: int = field(
        default_factory=lambda: int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
    )

    # Logging
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    def ensure_data_dirs(self) -> None:
        """Create necessary data directories if they don't exist."""
        dirs = [
            self.data_root_dir,
            self.vector_db.path,
            self.graph_db.path,
            self.relational_db.path,
        ]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)


# Singleton config instance
_config: Optional[CogneeConfig] = None


def get_config() -> CogneeConfig:
    """Return the global CogneeConfig instance, creating it if necessary."""
    global _config
    if _config is None:
        _config = CogneeConfig()
    return _config


def reset_config() -> None:
    """Reset the global config (useful for testing)."""
    global _config
    _config = None
