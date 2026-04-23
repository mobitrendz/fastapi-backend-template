from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Application configuration settings using Pydantic's BaseSettings. This class defines all the necessary configuration parameters for the application, including database connection details, JWT settings, and superuser credentials. The settings are loaded from environment variables, allowing for easy configuration in different environments (development, testing, production).
# The SQLALCHEMY_DATABASE_URI is computed based on the individual database connection parameters, providing a convenient way to access the full database URI for use in database connections. The use of BaseSettings allows for validation and type checking of the configuration parameters, ensuring that the application is configured correctly before it starts. The settings can be easily extended in the future to include additional configuration parameters as needed, and the use of environment variables allows for secure management of sensitive information like database credentials and secret keys without hardcoding them in the source code.


# The Settings class is instantiated at the end of the module, creating a global settings object that can be imported and used throughout the application to access configuration values. This promotes a centralized and consistent way to manage configuration across the entire codebase.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENVIRONMENT: str

    API_V1_STR: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SUPER_USER_NAME: str
    SUPER_USER_EMAIL: str
    SUPER_USER_PASSWORD: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @computed_field
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
