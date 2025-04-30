from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostListed import JobPostListed
from typing import Optional

class JobPostsListResponse(BaseModel):
    posts: list[JobPostListed]
    nextOffset: Optional[int] = None
