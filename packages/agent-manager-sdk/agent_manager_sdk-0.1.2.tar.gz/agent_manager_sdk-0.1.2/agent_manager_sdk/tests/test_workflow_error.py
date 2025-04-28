import pytest
from utils.miniapps.dnd import (
    validate_workflow,  # Adjust import based on where you put it
)


def test_workflow_with_no_nodes_raises_error():
    invalid_workflow = {
        "workflow_id": "test123",
        "workflow_name": "Empty Workflow",
        "graph": {
            "nodes": [],
            "edges": []
        },
        "output_keys": []
    }

    with pytest.raises(ValueError, match="Workflow must have at least one node."):
        validate_workflow(invalid_workflow)

def test_workflow_with_valid_start_llm_end():
    valid_workflow = {
        "workflow_id": "valid123",
        "workflow_name": "Simple Content Generator",
        "graph": {
            "nodes": [
                {
                    "id": "1",
                    "type": "custom",
                    "data": {
                        "type": "start",
                        "title": "Start",
                        "variables": [
                            {
                                "variable": "text",
                                "type": "text-input",
                                "required": True
                            }
                        ]
                    }
                },
                {
                    "id": "2",
                    "type": "llm",
                    "data": {
                        "type": "llm",
                        "title": "Generate Content",
                        "system": "You are a helpful assistant.",
                        "user": "Write something based on {text}",
                        "output_key": "short_content"
                    }
                },
                {
                    "id": "3",
                    "type": "custom",
                    "data": {
                        "type": "end",
                        "title": "End",
                        "variables": []
                    }
                }
            ],
            "edges": [
                {"source": "1", "target": "2", "data": {}},
                {"source": "2", "target": "3", "data": {}}
            ]
        },
        "output_keys": ["short_content"]
    }

    # Should not raise any error
    validate_workflow(valid_workflow)
