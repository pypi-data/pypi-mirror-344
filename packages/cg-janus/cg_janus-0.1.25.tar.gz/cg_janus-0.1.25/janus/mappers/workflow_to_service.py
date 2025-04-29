"Module to map the workflows to the services."

from janus.constants.workflow import Workflow
from janus.services.workflow_collect_qc_services import BalsamicCollectQCService


workflow_to_service = {
    Workflow.BALSAMIC: BalsamicCollectQCService(),
    Workflow.BALSAMIC_UMI: BalsamicCollectQCService(),
}
