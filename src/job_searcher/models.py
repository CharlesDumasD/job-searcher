from pydantic import BaseModel, HttpUrl


class JobListing(BaseModel):
    """Normalized job listing used by the agent tools."""

    title: str
    company: str
    location: str | None = None
    description: str | None = None
    url: HttpUrl | None = None
    source: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    remote: bool | None = None
    posted_at: str | None = None
