from typing import Annotated, Any, Self

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

# Application configuration settings using Pydantic's BaseSettings. This class defines all the necessary configuration parameters for the application, including database connection details, JWT settings, and superuser credentials. The settings are loaded from environment variables, allowing for easy configuration in different environments (development, testing, production).
# The SQLALCHEMY_DATABASE_URI is computed based on the individual database connection parameters, providing a convenient way to access the full database URI for use in database connections. The use of BaseSettings allows for validation and type checking of the configuration parameters, ensuring that the application is configured correctly before it starts. The settings can be easily extended in the future to include additional configuration parameters as needed, and the use of environment variables allows for secure management of sensitive information like database credentials and secret keys without hardcoding them in the source code.

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

# The Settings class is instantiated at the end of the module, creating a global settings object that can be imported and used throughout the application to access configuration values. This promotes a centralized and consistent way to manage configuration across the entire codebase.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    FRONTEND_HOST: str
    ENVIRONMENT: str

    PROJECT_NAME: str
    STACK_NAME: str

    API_V1_STR: str

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SMTP_TLS: bool = False
    SMTP_SSL: bool = False
    SMTP_PORT: int = 1025
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    SUPER_USER_NAME: str
    SUPER_USER_EMAIL: str
    SUPER_USER_PASSWORD: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # ty:ignore[missing-argument]
