from typing import TypedDict, Literal, Optional

class PipelineState(TypedDict):
    topic: str 
    research: str | None
    outline: str | None
    draft: str | None
    decision: Literal["approved", "rejected"] | None
    reason: str | None
    revision_count : int 
    next: Literal["researcher", "outliner", "writer", "editor", "__end__"] | None