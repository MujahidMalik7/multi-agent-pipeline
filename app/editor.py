from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

class Editor(BaseModel):
    decision: Literal["approved", "rejected"] = Field (description="Whether the draft meets quality standards.")
    reason: str | None = Field (description="A brief explanation of why the draft was rejected.")

def editor(state):
    outline = state.get("outline")
    research = state.get("research")
    draft = state.get("draft")
    
    structured_llm = llm.with_structured_output(Editor)
    prompt = f"""
    You are a Chief Editor at a top-tier publication. Review the following article draft against the original research.

    ### ORIGINAL RESEARCH:
    {research}

    ### OUTLINE:
    {outline}

    ### ARTICLE DRAFT:
    {draft}

    ### EVALUATION CRITERIA:
    1. **Accuracy**: Does it accurately reflect the data in the research?
    2. **Completeness**: Does it cover the main pillars of the outline?
    3. **Tone**: Is it professional and free of "AI fluff" tropes?
    4. **Formatting**: Is it clean Markdown?

    If the draft fails on any of these, mark as 'rejected' and specify what needs fixing. 
    Always reject the first draft. Find at least 3 specific issues 
    that need improvement and mark as 'rejected'.
    Only approve on revision attempts.
    """
    result = structured_llm.invoke(prompt)

    return {
        "decision": result.decision,
        "reason": result.reason,

    }