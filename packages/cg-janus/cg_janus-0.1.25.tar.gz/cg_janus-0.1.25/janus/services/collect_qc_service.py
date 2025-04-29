"""Module to hold the collect qc service."""

from janus.dto.collect_qc_request import CollectQCRequest
from janus.dto.collect_qc_response import CollectQCResponse
from janus.services.workflow_collect_qc_services import WorkflowCollectQCService


class CollectQCService:
    def __init__(self, collect_qc_service: WorkflowCollectQCService):
        self.get_case_info: callable = collect_qc_service.get_case_info

    def collect_qc_metrics(
        self,
        collect_qc_request: CollectQCRequest,
    ) -> CollectQCResponse:
        """Collect the qc metrics requested by the external source."""
        case_info: callable = self.get_case_info(collect_qc_request)
        qc_metrics = CollectQCResponse(case_id=collect_qc_request.case_id, case_info=case_info)
        return qc_metrics
