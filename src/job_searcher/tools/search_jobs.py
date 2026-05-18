from langchain_core.tools import tool

from job_searcher.models import JobListing


@tool
def search_jobs(
    query: str,
    location: str | None = None,
    remote: bool | None = None,
    limit: int = 5,
) -> list[dict[str, object]]:
    """Search for job listings matching the user's criteria."""
    mock_jobs = [
        JobListing(
            title="AI Engineer, Clinical Decision Support",
            company="CarePath AI",
            location="Paris, France",
            description=(
                "Build LLM and ML workflows for clinical decision support in "
                "hospital settings."
            ),
            url="https://example.com/jobs/carepath-ai-engineer",
            source="mock",
            salary_min=70000,
            salary_max=95000,
            remote=False,
            posted_at="2026-05-12",
        ),
        JobListing(
            title="Remote Healthcare ML Engineer",
            company="MedNLP Labs",
            location="Remote, Europe",
            description=(
                "Develop NLP models for clinical notes, patient triage, and "
                "medical coding workflows."
            ),
            url="https://example.com/jobs/mednlp-ml-engineer",
            source="mock",
            salary_min=85000,
            salary_max=120000,
            remote=True,
            posted_at="2026-05-14",
        ),
        JobListing(
            title="Data Scientist, Digital Health",
            company="BioSignal Health",
            location="Lyon, France",
            description=(
                "Analyze wearable and patient monitoring data to improve early "
                "risk detection."
            ),
            url="https://example.com/jobs/biosignal-data-scientist",
            source="mock",
            salary_min=60000,
            salary_max=82000,
            remote=False,
            posted_at="2026-05-10",
        ),
        JobListing(
            title="Machine Learning Platform Engineer",
            company="Hospital Systems Group",
            location="Remote, France",
            description=(
                "Own deployment infrastructure for healthcare ML models, "
                "monitoring, and governance."
            ),
            url="https://example.com/jobs/hsg-ml-platform",
            source="mock",
            salary_min=90000,
            salary_max=125000,
            remote=True,
            posted_at="2026-05-15",
        ),
    ]

    filtered_jobs = mock_jobs
    if location:
        location_lower = location.lower()
        filtered_jobs = [
            job
            for job in filtered_jobs
            if job.location and location_lower in job.location.lower()
        ]

    if remote is not None:
        filtered_jobs = [job for job in filtered_jobs if job.remote is remote]

    return [job.model_dump(mode="json") for job in filtered_jobs[:limit]]
