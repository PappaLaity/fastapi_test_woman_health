# from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Women Health API"
    VERSION: str = "1.0.0"
    
    # Model Paths
    CV_MODEL_PATH: str = "ml_models/logistic_regression.pkl"
    # CV_MODEL_PATH: str = "ml_models/breast_cancer_model.h5"
    # MODEL_CONFIG_PATH: str = "ml_models/model_config.json"
    
    # LLM Configuration
    LLM_PROVIDER: str = "ollama"  # "ollama" ou "anthropic"
    
    # Configuration Ollama
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"  # ou "mistral", "llama2", etc.
    
    # Configuration Anthropic (si utilisé)
    ANTHROPIC_API_KEY: str = ""
    LLM_MODEL: str = "claude-sonnet-4-20250514"
    
    # Paramètres LLM communs
    LLM_MAX_TOKENS: int = 1000
    LLM_TEMPERATURE: float = 0.7
    
    # Image Processing
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".dcm"]
    IMAGE_INPUT_SIZE: tuple = (224, 224)  # Taille pour le modèle
    
    # Security
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost", "http://localhost:8080"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()