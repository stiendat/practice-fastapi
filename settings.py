from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

def get_config(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)

POSTGRES_USER = get_config("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = get_config("POSTGRES_PASSWORD", default="123456")
POSTGRES_DB = get_config("POSTGRES_DB", default="library_db")
POSTGRES_PORT = get_config("POSTGRES_PORT", default="5432") 
POSTGRES_HOST = get_config("POSTGRES_HOST", "localhost")