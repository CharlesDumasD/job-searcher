import html

import httpx

from job_searcher.config import Settings
from job_searcher.models import JobListing

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def search_adzuna_jobs(
    settings: Settings,
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
    limit: int | None = None,
) -> list[JobListing]:
    """Search Adzuna jobs and return normalized listings."""
    if settings.adzuna_app_id is None or settings.adzuna_app_key is None:
        raise ValueError(
            "Adzuna credentials are missing. Set ADZUNA_APP_ID and "
            "ADZUNA_APP_KEY in your .env file."
        )

    results_per_page = limit or settings.adzuna_results_per_page
    url = f"{ADZUNA_BASE_URL}/{settings.adzuna_country}/search/1"
    params: dict[str, str | int] = {
        "app_id": settings.adzuna_app_id.get_secret_value(),
        "app_key": settings.adzuna_app_key.get_secret_value(),
        "content-type": "application/json",
        "results_per_page": results_per_page,
        "what": query,
    }

    if location:
        params["where"] = location
    if excluded_keywords:
        params["what_exclude"] = excluded_keywords
    if company:
        params["company"] = company
    if salary_min is not None:
        params["salary_min"] = salary_min
    if salary_max is not None:
        params["salary_max"] = salary_max
    if full_time is not None:
        params["full_time"] = int(full_time)
    if part_time is not None:
        params["part_time"] = int(part_time)
    if permanent is not None:
        params["permanent"] = int(permanent)
    if contract is not None:
        params["contract"] = int(contract)
    if max_days_old is not None:
        params["max_days_old"] = max_days_old
    if sort_by:
        params["sort_by"] = sort_by

    response = httpx.get(url, params=params, timeout=15)
    response.raise_for_status()
    payload = response.json()

    return [_parse_job(result) for result in payload.get("results", [])]


def _parse_job(result: dict[str, object]) -> JobListing:
    """Convert one Adzuna API result into a normalized job listing."""
    company = result.get("company")
    location = result.get("location")

    company_name = ""
    if isinstance(company, dict):
        company_name = str(company.get("display_name") or "")

    location_name = None
    if isinstance(location, dict):
        location_name = str(location.get("display_name") or "") or None

    description = result.get("description")
    if isinstance(description, str):
        description = html.unescape(description)

    return JobListing(
        title=str(result.get("title") or ""),
        company=company_name,
        location=location_name,
        description=description if isinstance(description, str) else None,
        url=result.get("redirect_url"),
        source="adzuna",
        salary_min=_parse_optional_int(result.get("salary_min")),
        salary_max=_parse_optional_int(result.get("salary_max")),
        posted_at=str(result.get("created") or "") or None,
    )


def _parse_optional_int(value: object) -> int | None:
    """Parse an optional numeric value as an integer."""
    if value is None:
        return None
    return int(float(str(value)))
