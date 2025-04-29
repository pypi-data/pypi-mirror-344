from http import HTTPStatus

from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

from janus.dto.collect_qc_request import CollectQCRequest
from janus.dto.collect_qc_response import CollectQCResponse
from janus.exceptions.exceptions import WorkflowNotSupportedError
from janus.server.utils import get_workflow_service
from janus.services.collect_qc_service import CollectQCService
from pydantic import ValidationError

from janus.services.workflow_collect_qc_services import WorkflowCollectQCService

collect_qc_router = APIRouter()


@collect_qc_router.get(
    "/collect_qc/",
    response_description="Collect qc metrics for a case.",
    response_model=CollectQCResponse,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
def collect_qc(
    collect_request: CollectQCRequest = Body(...),
) -> CollectQCResponse | JSONResponse:
    """Collect qc metrics for the external request."""
    try:
        workflow_service: WorkflowCollectQCService = get_workflow_service(collect_request.workflow)
        collect_service = CollectQCService(collect_qc_service=workflow_service)
        return collect_service.collect_qc_metrics(collect_qc_request=collect_request)
    except (ValueError, FileNotFoundError, ValidationError, WorkflowNotSupportedError) as error:
        return JSONResponse(content=repr(error), status_code=HTTPStatus.BAD_REQUEST)
