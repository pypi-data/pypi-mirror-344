from typing import Any, List

from .....core.workflow.entities.base_node_data_entities import BaseNodeData


class WorkflowNodeData(BaseNodeData):
    """
    LLM Node Data.
    """
    workflow_id: str
    inputs: dict[str, Any]
    output_keys: List[str] = []