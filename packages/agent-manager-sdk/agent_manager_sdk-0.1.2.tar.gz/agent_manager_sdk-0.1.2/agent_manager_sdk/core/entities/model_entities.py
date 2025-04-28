from enum import Enum


class ModelStatus(Enum):
    """
    Enum class for model status.
    """
    ACTIVE = "active"
    NO_CONFIGURE = "no-configure"
    QUOTA_EXCEEDED = "quota-exceeded"
    NO_PERMISSION = "no-permission"
    DISABLED = "disabled"
