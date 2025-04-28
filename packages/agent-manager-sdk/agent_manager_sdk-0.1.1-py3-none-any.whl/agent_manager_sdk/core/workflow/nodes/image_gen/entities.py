from typing import Any, Literal, Optional, Union

from pydantic import BaseModel

from .....core.prompt.entities.advanced_prompt_entities import (
    ChatModelMessage,
    CompletionModelPromptTemplate,
    MemoryConfig,
)
from .....core.workflow.entities.base_node_data_entities import BaseNodeData
from .....core.workflow.entities.variable_entities import VariableSelector


class ContextConfig(BaseModel):
    """
    Context Config.
    """
    enabled: bool
    variable_selector: Optional[list[str]] = None
    
class ImageGenNodeData(BaseNodeData):
    """
    LLM Node Data.
    """
    prompt: str
    output_key: str
