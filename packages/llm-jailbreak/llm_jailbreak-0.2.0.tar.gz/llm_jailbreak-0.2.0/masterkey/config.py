from pydantic import BaseModel

class MasterKeyConfig(BaseModel):
    api_key: str  # 必需：DeepSeek API Key
    model_name: str = "deepseek-chat"
    max_retries: int = 3
    timeout: int = 30
    temperature: float = 0.7
