from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import TradeRouteOptimizeRequest, TradeRouteOptimizeResponse
from backend.services.trade_route_service import TradeRouteService

router = APIRouter(tags=["Trade Route Optimization"])
trade_route_service = TradeRouteService()


@router.post("/trade-route/optimize", response_model=TradeRouteOptimizeResponse)
def optimize_trade_route(request: TradeRouteOptimizeRequest):
    """
    Optimize vessel passage route using constraint-aware NetworkX A* route engine.
    """
    try:
        return trade_route_service.optimize_route(request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Trade route optimization error: {str(e)}"
        )
