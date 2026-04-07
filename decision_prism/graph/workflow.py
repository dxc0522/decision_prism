"""构建辩论 StateGraph。"""

from langgraph.graph import END, StateGraph

from decision_prism.graph.edges import (
    route_after_dispatch,
    route_after_intent,
    route_after_research,
    route_after_round1,
    route_after_round2,
    route_after_round3,
    route_after_synthesis,
)
from decision_prism.graph.nodes import (
    analysis_node,
    debate_round1_node,
    debate_round2_node,
    debate_round3_node,
    dispatch_experts_node,
    intent_parsing_node,
    research_node,
    synthesize_report_node,
)
from decision_prism.models.state import DebateState


def build_debate_graph() -> StateGraph:
    """构建并编译辩论 StateGraph。"""
    workflow = StateGraph(DebateState)

    # 添加节点
    workflow.add_node("intent_parsing", intent_parsing_node)
    workflow.add_node("dispatch_experts", dispatch_experts_node)
    workflow.add_node("research", research_node)
    workflow.add_node("debate_round1", debate_round1_node)
    workflow.add_node("debate_round2", debate_round2_node)
    workflow.add_node("debate_round3", debate_round3_node)
    workflow.add_node("synthesize_report", synthesize_report_node)
    workflow.add_node("analysis", analysis_node)

    # 入口点
    workflow.set_entry_point("intent_parsing")

    # 线性边（未来的条件路由存根）
    workflow.add_conditional_edges(
        "intent_parsing",
        route_after_intent,
        {
            "dispatch_experts": "dispatch_experts",
        },
    )
    workflow.add_conditional_edges(
        "dispatch_experts",
        route_after_dispatch,
        {
            "research": "research",
        },
    )
    workflow.add_conditional_edges(
        "research",
        route_after_research,
        {
            "debate_round1": "debate_round1",
        },
    )
    workflow.add_conditional_edges(
        "debate_round1",
        route_after_round1,
        {
            "debate_round2": "debate_round2",
        },
    )
    workflow.add_conditional_edges(
        "debate_round2",
        route_after_round2,
        {
            "debate_round3": "debate_round3",
        },
    )
    workflow.add_conditional_edges(
        "debate_round3",
        route_after_round3,
        {
            "synthesize_report": "synthesize_report",
        },
    )
    workflow.add_conditional_edges(
        "synthesize_report",
        route_after_synthesis,
        {
            "analysis": "analysis",
        },
    )
    workflow.add_edge("analysis", END)

    return workflow.compile()
