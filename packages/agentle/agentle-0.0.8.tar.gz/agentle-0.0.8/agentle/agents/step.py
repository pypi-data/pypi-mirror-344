from collections.abc import Sequence
from rsb.models.base_model import BaseModel

from agentle.generations.models.message_parts.tool_execution_suggestion import (
    ToolExecutionSuggestion,
)


class Step(BaseModel):
    called_tools: Sequence[ToolExecutionSuggestion]
