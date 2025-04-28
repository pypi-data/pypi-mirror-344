from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class DatasetRetrieveConfigEntity(BaseModel):
    """
    Dataset Retrieve Config Entity.
    """

    class RetrieveStrategy(Enum):
        """
        Dataset Retrieve Strategy.
        'single' or 'multiple'
        """
        SINGLE = 'single'
        MULTIPLE = 'multiple'

        @classmethod
        def value_of(cls, value: str):
            """
            Get value of given mode.

            :param value: mode value
            :return: mode
            """
            for mode in cls:
                if mode.value == value:
                    return mode
            raise ValueError(f'invalid retrieve strategy value {value}')

    query_variable: Optional[str] = None  # Only when app mode is completion

    retrieve_strategy: RetrieveStrategy
    top_k: Optional[int] = None
    score_threshold: Optional[float] = None
    reranking_model: Optional[dict] = None
    
class VariableEntity(BaseModel):
    """
    Variable Entity.
    """
    class Type(Enum):
        TEXT_INPUT = 'text-input'
        SELECT = 'select'
        PARAGRAPH = 'paragraph'
        NUMBER = 'number'

        @classmethod
        def value_of(cls, value: str) -> 'VariableEntity.Type':
            """
            Get value of given mode.

            :param value: mode value
            :return: mode
            """
            for mode in cls:
                if mode.value == value:
                    return mode
            raise ValueError(f'invalid variable type value {value}')

    variable: str
    # label: str
    description: Optional[str] = None
    # type: Type
    required: bool = False
    # max_length: Optional[int] = None
    # options: Optional[list[str]] = None
    default: Optional[str] = None
    # hint: Optional[str] = None

class FileExtraConfig(BaseModel):
    """
    File Upload Entity.
    """
    image_config: Optional[dict[str, Any]] = None