import pytest
from utils.miniapps.dnd import validate_workflow


def test_workflow_with_invalid_node_raises_error():
    invalid_workflow = {
        "workflow_id": "invalid456",
        "workflow_name": "Invalid Node Workflow",
        "graph": {
            "nodes": [
                {
                    "id": "1",
                    "type": "custom",
                    "data": {
                        # "type": "start" missing on purpose
                        "title": "Start",
                        "variables": []
                    }
                }
            ],
            "edges": []
        },
        "output_keys": []
    }

    with pytest.raises(ValueError, match="Node missing required 'type' field"):
        validate_workflow(invalid_workflow)
