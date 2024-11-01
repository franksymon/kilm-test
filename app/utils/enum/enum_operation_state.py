from enum import Enum
class OperationState(str, Enum):
    UPDATE = "UPDATE"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN PROGRESS"

