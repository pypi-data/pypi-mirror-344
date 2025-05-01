from enum import Enum


class ToolSourceType(str, Enum):
    """Defines what a tool was derived from"""

    python = "python"
    json = "json"
class ToolType(str, Enum):
    CUSTOM = "custom"
    LUANN_CORE = "luann_core"
    LUANN_MEMORY_CORE = "luann_memory_core"
    LUANN_MULTI_AGENT_CORE = "luann_multi_agent_core"


class JobType(str, Enum):
    JOB = "job"
    RUN = "run"
