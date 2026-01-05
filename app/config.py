from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    SERVICE_NAME: str = "skillsieve_parser_micro"
    VERSION: str = "0.0.1"
    REDIS_URL: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    NEST_CALLBACK_URL: str
    NEST_INTERNAL_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
