from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies import enforce_write_rate_limit, get_workshop_service, require_authenticated, require_csrf
from models.workshop import WorkshopPayload
from services.workshop_service import WorkshopService

router = APIRouter(prefix="/api", tags=["workshops"])


@router.get("/workshops", dependencies=[Depends(require_authenticated)])
async def list_workshops(
    q: str | None = Query(default=None, max_length=80),
    category: str | None = Query(default=None, max_length=40),
    workshop_service: WorkshopService = Depends(get_workshop_service),
) -> dict:
    return await workshop_service.get_dashboard_snapshot(search_query=q, category=category)


@router.get("/workshops/{workshop_id}", dependencies=[Depends(require_authenticated)])
async def get_workshop(
    workshop_id: str,
    workshop_service: WorkshopService = Depends(get_workshop_service),
) -> dict:
    workshop = await workshop_service.get_workshop(workshop_id)
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found.",
        )
    return {"workshop": workshop}


@router.post(
    "/workshops",
    dependencies=[
        Depends(require_authenticated),
        Depends(require_csrf),
        Depends(enforce_write_rate_limit),
    ],
    status_code=status.HTTP_201_CREATED,
)
async def create_workshop(
    payload: WorkshopPayload,
    workshop_service: WorkshopService = Depends(get_workshop_service),
) -> dict:
    workshop = await workshop_service.create_workshop(payload)
    return {"detail": "Workshop created successfully.", "workshop": workshop}


@router.put(
    "/workshops/{workshop_id}",
    dependencies=[
        Depends(require_authenticated),
        Depends(require_csrf),
        Depends(enforce_write_rate_limit),
    ],
)
async def update_workshop(
    workshop_id: str,
    payload: WorkshopPayload,
    workshop_service: WorkshopService = Depends(get_workshop_service),
) -> dict:
    workshop = await workshop_service.update_workshop(workshop_id, payload)
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found.",
        )
    return {"detail": "Workshop updated successfully.", "workshop": workshop}


@router.delete(
    "/workshops/{workshop_id}",
    dependencies=[
        Depends(require_authenticated),
        Depends(require_csrf),
        Depends(enforce_write_rate_limit),
    ],
)
async def delete_workshop(
    workshop_id: str,
    workshop_service: WorkshopService = Depends(get_workshop_service),
) -> dict:
    workshop = await workshop_service.get_workshop(workshop_id)
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found.",
        )

    await workshop_service.delete_workshop(workshop_id)
    return {"detail": "Workshop deleted successfully.", "workshop_id": workshop_id}
