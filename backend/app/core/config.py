from pydantic_settings import BaseSettings
from pydantic import Extra

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    AZURE_API_VERSION: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_DEPLOYMENT_NAME: str
    AZURE_OPENAI_KEY: str
    BLOB_CONNECTION_STRING: str
    CONTAINER_NAME: str

    class Config:
        env_file = ".env"
        extra = Extra.allow

settings = Settings()
