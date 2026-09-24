from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # parametre de comment charger le fichier 
    # env_file : charger le fichier env sinon il prend les valeur du systeme
    # extra="ignore" : ignore les variables non charge, inutile
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str
    algorithm: str = "HS256"
    token_expire_min: int = 30
    database_url: str
    cors_origin: str = "http://localhost:5173"


settings = Settings()