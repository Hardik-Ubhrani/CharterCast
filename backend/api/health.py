from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health():
    """
    Health check endpoint returning system status and service details.
    """
    return {
        "status": "healthy",
        "service": "PORTWISE AI Backend",
        "version": "0.1.0"
    }
