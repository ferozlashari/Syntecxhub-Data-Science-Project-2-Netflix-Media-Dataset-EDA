from fastapi import APIRouter

from app.analysis import netflix_analysis
from app.data.generate_netflix import generate as generate_netflix_data

router = APIRouter(prefix="/api/netflix", tags=["netflix"])

_cache = {"result": None}


def ensure_data():
    if not netflix_analysis.DATA_FILE.exists():
        generate_netflix_data()


@router.get("/analysis")
def get_analysis():
    ensure_data()
    if _cache["result"] is None:
        _cache["result"] = netflix_analysis.run()
    return _cache["result"]


@router.get("/analysis/refresh")
def refresh_analysis():
    generate_netflix_data()
    _cache["result"] = netflix_analysis.run()
    return _cache["result"]
