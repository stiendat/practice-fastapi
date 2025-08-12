from datetime import datetime

from pydantic import BaseModel, field_serializer

class TimestampMixin(BaseModel):
    """Mixin that adds timestamp columns to a model."""
    
    created_at: datetime
    updated_at: datetime
    
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime | None) -> str | None:
        if dt is None:
            return None
        return dt.strftime("%Y-%m-%d %H:%M:%S")  # Format as expected by the test
    class Config:
        from_attributes = True