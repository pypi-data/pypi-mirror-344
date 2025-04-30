from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class JobPostsListPayload(BaseModel):
    accountId: UUID
    offset: Optional[int] = None
