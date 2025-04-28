from enum import Enum

from pydantic import BaseModel


class QueueEvent(Enum):
    """
    QueueEvent enum
    """
    LLM_CHUNK = "llm_chunk"
    TEXT_CHUNK = "text_chunk"
    AGENT_MESSAGE = "agent_message"
    MESSAGE_REPLACE = "message_replace"
    MESSAGE_END = "message_end"
    ADVANCED_CHAT_MESSAGE_END = "advanced_chat_message_end"
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_SUCCEEDED = "workflow_succeeded"
    WORKFLOW_FAILED = "workflow_failed"
    ITERATION_START = "iteration_start"
    ITERATION_NEXT = "iteration_next"
    ITERATION_COMPLETED = "iteration_completed"
    NODE_STARTED = "node_started"
    NODE_SUCCEEDED = "node_succeeded"
    NODE_FAILED = "node_failed"
    RETRIEVER_RESOURCES = "retriever_resources"
    ANNOTATION_REPLY = "annotation_reply"
    AGENT_THOUGHT = "agent_thought"
    MESSAGE_FILE = "message_file"
    ERROR = "error"
    PING = "ping"
    STOP = "stop"


class AppQueueEvent(BaseModel):
    """
    QueueEvent entity
    """
    event: QueueEvent

