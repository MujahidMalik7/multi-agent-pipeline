from langgraph.graph import StateGraph, START, END
from researcher import researcher
from outliner import outliner
from writer import writer
from editor import editor
from state import PipelineState
from supervisor import supervisor 

workflow = StateGraph(PipelineState)

workflow.add_node("supervisor", supervisor)
workflow.add_node("researcher", researcher)
workflow.add_node("outliner", outliner)
workflow.add_node("writer", writer)
workflow.add_node("editor", editor)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges("supervisor", lambda state: state["next"])
workflow.add_edge("researcher","supervisor")
workflow.add_edge("outliner","supervisor")
workflow.add_edge("writer","supervisor")
workflow.add_edge("editor","supervisor")

pipeline = workflow.compile()