from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import ProbeLaunchRequest, ProbeMoveRequest, ProbeResponse, AllProbesResponse
from app.services.probe_service import ProbeService, ProbeNotFoundError, InvalidCommandError
from .dependencies import get_probe_service

router = APIRouter()

@router.post("/probes", response_model=ProbeResponse, status_code=status.HTTP_201_CREATED)
def launch_probe(request: ProbeLaunchRequest, service: ProbeService = Depends(get_probe_service)):
    try:
        probe = service.launch_probe(
            max_x=request.x,
            max_y=request.y,
            direction_str=request.direction.value
        )

        return ProbeResponse(
            id=probe.id,
            x=probe.position.x,
            y=probe.position.y,
            direction=probe.current_direction
        )
    except InvalidCommandError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/probes/{probe_id}/move", response_model=ProbeResponse)
def move_probe(
    probe_id: str,
    request: ProbeMoveRequest,
    service: ProbeService = Depends(get_probe_service)
):
    try:
        probe = service.move_probe(probe_id, request.commands)
        return ProbeResponse(
            id=probe.id,
            x=probe.position.x,
            y=probe.position.y,
            direction=probe.current_direction
        )
    except ProbeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCommandError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/probes", response_model=AllProbesResponse)
def get_all_probes(service: ProbeService = Depends(get_probe_service)):
    probes = service.get_all_probes()
    probe_responses = [
        ProbeResponse(
            id=p.id,
            x=p.position.x,
            y=p.position.y,
            direction=p.current_direction
        ) for p in probes
    ]
    return AllProbesResponse(probes=probe_responses)