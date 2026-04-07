"""辩论图的路由函数。

MVP 使用线性路由（始终进入下一轮）。
这些函数为未来的条件路由预留的存根
（例如，达成共识时提前退出、质量门控等）。
"""

from decision_prism.models.state import DebateState


def route_after_intent(state: DebateState) -> str:
    """始终进入调度阶段。"""
    return "dispatch_experts"


def route_after_dispatch(state: DebateState) -> str:
    """始终进入研究阶段。"""
    return "research"


def route_after_research(state: DebateState) -> str:
    """Always proceed to Round 1."""
    return "debate_round1"


def route_after_round1(state: DebateState) -> str:
    """Always proceed to Round 2.
    Future: Check consensus — early exit if agreement threshold met.
    """
    return "debate_round2"


def route_after_round2(state: DebateState) -> str:
    """Always proceed to Round 3.
    Future: Quality gate — if statements lack sufficient depth, repeat.
    """
    return "debate_round3"


def route_after_round3(state: DebateState) -> str:
    """Always proceed to synthesis."""
    return "synthesize_report"


def route_after_synthesis(state: DebateState) -> str:
    """Always proceed to analysis."""
    return "analysis"
