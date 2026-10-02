from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_database_session

from app.modules.integracoes.thingspeak.exceptions import (
    ThingSpeakConfigurationError,
    ThingSpeakConnectionError,
    ThingSpeakError,
    ThingSpeakHTTPError,
    ThingSpeakInvalidResponseError,
    ThingSpeakTimeoutError,
)
from app.modules.integracoes.thingspeak.schemas import (
    ThingSpeakFeed,
    ThingSpeakMappingResult,
    ThingSpeakSyncSummary,
    ThingSpeakStatusResponse,
)
from app.modules.integracoes.thingspeak.service import ThingSpeakService

router = APIRouter(prefix="/api/v1/integracoes/thingspeak", tags=["integracoes", "thingspeak"])


@router.get("/status", response_model=ThingSpeakStatusResponse)
def get_status() -> ThingSpeakStatusResponse:
    return ThingSpeakService.from_settings().get_status()


@router.get("/feeds", response_model=ThingSpeakMappingResult)
async def get_feeds(results: int | None = Query(default=10, ge=1, le=8000)) -> ThingSpeakMappingResult:
    try:
        return await ThingSpeakService.from_settings().get_mapped_feeds(results=results)
    except ThingSpeakError as exc:
        _raise_http_error(exc)


@router.get("/ultima-leitura", response_model=ThingSpeakFeed | None)
async def get_latest_feed() -> ThingSpeakFeed | None:
    try:
        return await ThingSpeakService.from_settings().get_latest_feed()
    except ThingSpeakError as exc:
        _raise_http_error(exc)


@router.post("/sincronizar", response_model=ThingSpeakSyncSummary)
async def sincronizar_feeds(
    results: int | None = Query(default=100, ge=1, le=8000),
    db: Session = Depends(get_database_session),
) -> ThingSpeakSyncSummary:
    try:
        return await ThingSpeakService.from_settings().sincronizar_feeds(db=db, results=results)
    except ThingSpeakError as exc:
        _raise_http_error(exc)


def _raise_http_error(exc: ThingSpeakError) -> None:
    if isinstance(exc, ThingSpeakConfigurationError):
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if isinstance(exc, ThingSpeakTimeoutError):
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    if isinstance(exc, ThingSpeakConnectionError):
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    if isinstance(exc, ThingSpeakHTTPError):
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    if isinstance(exc, ThingSpeakInvalidResponseError):
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    raise HTTPException(status_code=500, detail="Unexpected ThingSpeak integration error.") from exc
