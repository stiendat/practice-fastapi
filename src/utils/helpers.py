import uuid
from datetime import datetime, timedelta


def generate_uuid() -> str:
    """
    Generate a UUID string for use as primary key.
    """
    return str(uuid.uuid4())


def get_default_return_date(days: int = 14) -> datetime:
    """
    Get default return date (14 days from now).
    """
    return datetime.now() + timedelta(days=days)


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    """
    import re
    digits_only = re.sub(r'\D', '', phone)
    return 10 <= len(digits_only) <= 15 