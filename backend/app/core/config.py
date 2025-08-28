from pydantic import BaseModel
import os


class Settings(BaseModel):
    project_name: str = os.getenv("PROJECT_NAME", "carbon-footprint-poc")
    database_url: str = os.getenv("DATABASE_URL", "")
    secret_key: str = os.getenv("SECRET_KEY", "changeme")
    cors_origins: str = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "uploads")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")


settings = Settings()