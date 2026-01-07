from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel

class Resume(BaseModel):
    id: UUID = uuid4()
    filename: str
    upload_time: datetime = datetime.utcnow()
