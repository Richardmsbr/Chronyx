"""
Chronyx Community Edition - Configuration Management
Centralized settings with security best practices.
"""
import os
import secrets
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings with secure defaults."""

    # Application
    app_name: str = "Chronyx Community"
    app_version: str = "1.0.0"
    environment: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )
    debug: bool = False
    log_level: str = "INFO"

    # AI Providers
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key"
    )
    openai_base_url: Optional[str] = Field(
        default=None,
        description="OpenAI API base URL (for proxies)"
    )
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key"
    )

    # Model Configuration
    default_model: str = "gpt-4-turbo"
    fallback_model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7
    max_retries: int = 3
    timeout: int = 30

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./chronyx.db",
        description="Database connection string"
    )
    database_pool_size: int = 5
    database_pool_overflow: int = 10

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 60
    rate_limit_window: int = 60  # seconds

    # Email (SMTP)
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from: Optional[str] = None
    smtp_use_tls: bool = True

    # Security
    secret_key: str = Field(
        default_factory=lambda: os.environ.get(
            "SECRET_KEY",
            secrets.token_urlsafe(32)
        ),
        description="Secret key for encryption"
    )
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    cors_origins: List[str] = ["http://localhost:3000"]

    # Logging
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None

    # Agent Configuration
    max_conversation_history: int = 50
    context_window_size: int = 10
    enable_memory_persistence: bool = True

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = {"development", "staging", "production", "testing"}
        if v.lower() not in allowed:
            raise ValueError(f"environment must be one of: {allowed}")
        return v.lower()

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of: {allowed}")
        return v.upper()

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"

    @property
    def has_openai(self) -> bool:
        """Check if OpenAI is configured."""
        return self.openai_api_key is not None

    @property
    def has_anthropic(self) -> bool:
        """Check if Anthropic is configured."""
        return self.anthropic_api_key is not None

    @property
    def has_ai_provider(self) -> bool:
        """Check if any AI provider is configured."""
        return self.has_openai or self.has_anthropic

    def get_preferred_provider(self) -> str:
        """Get the preferred AI provider based on configuration."""
        if self.has_openai:
            return "openai"
        elif self.has_anthropic:
            return "anthropic"
        raise ValueError("No AI provider configured")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings()
