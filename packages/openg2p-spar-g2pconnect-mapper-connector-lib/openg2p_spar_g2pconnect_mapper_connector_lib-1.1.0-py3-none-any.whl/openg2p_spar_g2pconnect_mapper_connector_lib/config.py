from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="mapper_connector_", env_file=".env", extra="allow"
    )

    private_key: str = ""
    sender_id: str = ""
    issuer: str = ""
    audience: str = ""
