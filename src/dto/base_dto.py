from datetime import datetime
from pydantic import BaseModel

class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }