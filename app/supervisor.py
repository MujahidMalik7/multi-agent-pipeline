def supervisor(state):
    research = state.get("research")
    outline = state.get("outline")
    draft = state.get("draft")
    decision = state.get("decision")
    revision_count = state.get("revision_count")

    if revision_count >=2:
        return {"next": "__end__"}
    if research is None:
        return {"next": "researcher"}
    if outline is None:
        return {"next": "outliner"}
    if draft is None:
        return {"next": "writer"}
    if decision is None:
        return {"next": "editor"}
    if decision == "approved":
        return {"next": "__end__"}
    elif decision == "rejected":
        return {"next": "writer"}