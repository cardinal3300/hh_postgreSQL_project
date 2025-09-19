import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(key: str) -> Optional[str]:
    """Возвращает значение переменной окружения по ключу."""
    return os.getenv(key)
