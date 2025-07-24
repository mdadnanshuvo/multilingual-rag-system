from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_check() -> dict:
    """
    Checks the health status of the application.

    Returns:
        dict: A dictionary containing the health status.
    """
    return {"status": "ok"}
