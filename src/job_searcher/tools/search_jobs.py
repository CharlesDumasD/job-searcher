from langchain_core.tools import tool

from job_searcher.config import get_settings
from job_searcher.services.adzuna import search_adzuna_jobs


@tool
def search_jobs(
    query: str,
    location: str | None = None,
    excluded_keywords: str | None = None,
    company: str | None = None,
    salary_min: int | None = None,
    salary_max: int | None = None,
    full_time: bool | None = None,
    part_time: bool | None = None,
    permanent: bool | None = None,
    contract: bool | None = None,
    max_days_old: int | None = None,
    sort_by: str | None = None,
    limit: int = 5,
) -> list[dict[str, object]]:
    """Search jobs with Adzuna API filters explicitly requested by the user."""
    jobs = search_adzuna_jobs(
        settings=get_settings(),
        query=query,
        location=location,
        excluded_keywords=excluded_keywords,
        company=company,
        salary_min=salary_min,
        salary_max=salary_max,
        full_time=full_time,
        part_time=part_time,
        permanent=permanent,
        contract=contract,
        max_days_old=max_days_old,
        sort_by=sort_by,
        limit=limit,
    )
    return [job.model_dump(mode="json") for job in jobs]
