
from copy import deepcopy
from typing import Any, Optional, cast

import requests

from .....config import Config
from .....core.workflow.entities.base_node_data_entities import BaseNodeData
from .....core.workflow.entities.node_entities import NodeRunResult, NodeType
from .....core.workflow.entities.variable_pool import VariablePool
from .....core.workflow.nodes.base_node import BaseNode
from .....core.workflow.nodes.workflow_node.entities import WorkflowNodeData
from .....core.workflow.utils.variable_template_parser import populate_fstring
from .....models.workflow import WorkflowNodeExecutionStatus


class WorkflowNode(BaseNode):
    _node_data_cls = WorkflowNodeData
    node_type = NodeType.WORKFLOW

    def _run(self, variable_pool: VariablePool) -> NodeRunResult:
        """
        Run node
        :param variable_pool: variable pool
        :return:
        """
        node_data = cast(self._node_data_cls, deepcopy(self.node_data))

        for key, value in node_data.inputs.items():
            node_data.inputs[key] = populate_fstring(value, {**variable_pool.user_inputs, **variable_pool.outputs})
        
        workflow_id = node_data.workflow_id
        inputs = node_data.inputs
        output_keys = node_data.output_keys if hasattr(node_data, 'output_keys') else None
        
        
        
        result = self._run_inner_workflow(workflow_id, inputs)
        if output_keys:
            result = {key: result[key] for key in result if key in output_keys}
        print('SUBFLOW OUTPUT: ', result)
        return NodeRunResult(
            status=WorkflowNodeExecutionStatus.SUCCEEDED,
            inputs=inputs,
            outputs=result
        )

    @classmethod
    def _extract_variable_selector_to_variable_mapping(cls, node_data: BaseNodeData) -> dict[str, list[str]]:
        """
        Extract variable selector to variable mapping
        :param node_data: node data
        :return:
        """
        return {}

    def _run_inner_workflow(self, workflow_id: str, inputs: dict[str, Any]) -> dict[str, Any]:
        """
        Run inner workflow
        :param workflow_id: workflow id
        :param inputs: inputs
        :return:
        """
        
        workflow_endpoint = Config.WORKFLOW_ENDPOINT
        
        with requests.session() as s:
            data={
                'workflow_id': workflow_id,
                'user_id': '1',
                'inputs': inputs
            }
            r = s.post(workflow_endpoint, json=data)
            output = r.json()
            print(output)
            return output
            
            