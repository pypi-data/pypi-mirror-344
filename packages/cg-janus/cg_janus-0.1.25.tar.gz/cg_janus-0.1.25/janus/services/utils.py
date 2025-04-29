from janus.dto.collect_qc_request import CollectQCRequest
from janus.mappers.tag_to_parse_function import tag_to_parse_function


def format_sample_metrics(collected_metrics: list[dict], sample_id: str) -> dict:
    """Format the metrics for a sample."""
    sample_metrics: dict = {"sample_id": sample_id}
    for collected_metric in collected_metrics:
        for sample, metric in collected_metric.items():
            if sample == sample_id:
                sample_metrics.update(metric)
    return sample_metrics


def get_formatted_sample_metrics(collected_metrics: list[dict], sample_ids: list[str]) -> list:
    """Get formatted sample metrics."""
    formatted_sample_metrics: list = []
    for sample_id in sample_ids:
        collected_sample_metrics: dict = format_sample_metrics(
            collected_metrics=collected_metrics, sample_id=sample_id
        )
        formatted_sample_metrics.append(collected_sample_metrics)
    return formatted_sample_metrics


def get_case_metrics(collected_metrics: list[dict], case_id: str) -> dict:
    """Get case metrics."""
    case_metrics: list = []
    for metric in collected_metrics:
        for key in metric.keys():
            if key == case_id:
                case_metrics.append(metric[key])
    return {case_id: case_metrics}


def collect_metrics(request: CollectQCRequest) -> list[dict]:
    """Collect the metrics for the files provided in the request."""
    collected_metrics: list[callable] = []
    for file_path_and_tag in request.files:
        parse_function = tag_to_parse_function[file_path_and_tag.tag]
        collected_metrics.append(
            parse_function(
                file_path=file_path_and_tag.file_path,
                sample_ids=request.sample_ids,
                tag=file_path_and_tag.tag,
                case_id=request.case_id,
            )
        )
    return collected_metrics
