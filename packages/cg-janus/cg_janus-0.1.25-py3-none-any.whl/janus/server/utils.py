"""Utilities for the server module."""

from janus.constants.workflow import Workflow
from janus.exceptions.exceptions import WorkflowNotSupportedError
from janus.mappers.workflow_to_service import workflow_to_service
from janus.services.workflow_collect_qc_services import WorkflowCollectQCService


def get_workflow_service(workflow: Workflow) -> WorkflowCollectQCService:
    """Get the workflow service."""
    if workflow not in workflow_to_service.keys():
        raise WorkflowNotSupportedError(
            f"Janus does not support parsing of QC metrics for {workflow})"
        )
    return workflow_to_service[workflow]
