from datetime import datetime
from typing import Any

class BaseModel:
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 