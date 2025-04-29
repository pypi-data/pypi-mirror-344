"""Balsamic Collect QC service."""

from abc import ABC

from janus.constants.FileTag import FileTag
from janus.dto.collect_qc_request import CollectQCRequest
from janus.models.workflow.balsamic import Balsamic
from janus.services.utils import get_formatted_sample_metrics, get_case_metrics, collect_metrics


class WorkflowCollectQCService(ABC):
    """
    Abstract class for workflow collect QC service.

    This abstract base class provides a common interface for collecting quality control data in workflows.
    It defines a single method, ``get_case_info``, which must be implemented by any concrete subclass.

    .. note::
        This is an abstract class and cannot be instantiated directly. Instead, it should be inherited
        to create concrete subclasses that implement the required methods.
    """

    def get_case_info(self, request: CollectQCRequest) -> None:
        """
        Get the case information.

        This method takes a ``CollectQCRequest`` object as input and performs any necessary data collection or processing.
        It is intended for implementation by concrete subclasses of this abstract class.

        :param CollectQCRequest request: A ``CollectQCRequest`` object containing relevant information.

        :returns: None
        :rtype: NoneType
        """
        pass


class BalsamicCollectQCService(WorkflowCollectQCService):
    """
    Balsamic Collect QC service.

    This class provides a way to collect and process data for Balsamic workflows.
    It inherits from :class:`WorkflowCollectQCService`, which provides common functionality for collecting data.

    .. seealso:: :class:`WorkflowCollectQCService`
    """

    @staticmethod
    def _extract_somalier_metrics(case_metrics: dict) -> dict:
        """
        Extract Somalier metrics from case metrics.

        This method takes a dictionary of case metrics and returns the extracted Somalier metrics.
        It assumes that each metric in the input dictionary has a ``SOMALIER`` key, which contains the relevant data.

        :param dict case_metrics: A dictionary containing case metrics.

        :raises ValueError: If no Somalier entry is found in the case metrics.

        :returns: The extracted Somalier metrics.
        :rtype: dict
        """
        for metric in case_metrics:
            somalier_metrics = metric[FileTag.SOMALIER]
            if not somalier_metrics:
                raise ValueError("No Somalier entry found.")
            return somalier_metrics

    def get_case_info(
        self,
        request: CollectQCRequest,
    ) -> Balsamic:
        """
        Collect MultiQC metrics for the Balsamic workflow.

        This method takes a ``CollectQCRequest`` object and returns an instance of the :class:`Balsamic` class.
        It collects data from various sources, including case metrics, sample IDs, and workflows.

        :param CollectQCRequest request: A ``CollectQCRequest`` object containing relevant information.

        :returns: An instance of the :class:`Balsamic` class with collected data.
        :rtype: Balsamic
        """
        collected_metrics = collect_metrics(request)
        sample_metrics = get_formatted_sample_metrics(
            collected_metrics=collected_metrics, sample_ids=request.sample_ids
        )
        case_metrics = get_case_metrics(
            collected_metrics=collected_metrics, case_id=request.case_id
        )
        somalier_metrics = self._extract_somalier_metrics(case_metrics[request.case_id])
        return Balsamic(
            samples=sample_metrics,
            somalier=somalier_metrics,
            workflow=request.workflow_info,
        )
