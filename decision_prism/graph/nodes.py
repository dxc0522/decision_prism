"""All graph nodes for the debate workflow."""

import asyncio

import nest_asyncio

nest_asyncio.apply()

from decision_prism.models.state import DebateState  # noqa: E402


def _run(coro: asyncio.Future) -> str:
    """Run an async coroutine from sync context."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


def intent_parsing_node(state: DebateState) -> dict:
    """Extract domains from query using keyword dispatch."""
    from decision_prism.models.domain import dispatch_agents

    query = state["query"]
    agents = dispatch_agents(query)
    domains = [a["domain"] for a in agents]
    return {
        "detected_domains": domains,
        "selected_experts": agents,
        "debate_roles": ["government_regulator", "enterprise_market", "individual_user"],
    }


def dispatch_experts_node(state: DebateState) -> dict:
    """Confirm expert assignments (already done by intent parsing)."""
    return {}


def research_node(state: DebateState) -> dict:
    """Run Tavily search for each expert domain."""
    from decision_prism.config import get_settings
    from decision_prism.tools.tavily_search import tavily_search

    query = state["query"]
    materials: dict[str, list[str]] = {}
    errors = []

    # Only do one search for the full query + top domain to save API calls
    top_domain = state["detected_domains"][0] if state["detected_domains"] else "general"
    search_query = f"{query} {top_domain}"

    try:
        settings = get_settings()
        if settings.tavily_api_key:
            results = tavily_search(search_query, settings.tavily_api_key, num_results=5)
            materials[top_domain] = [r["content"] for r in results if r.get("content")]
        else:
            materials[top_domain] = [f"[Tavily not configured for domain: {top_domain}]"]
    except Exception as e:
        materials[top_domain] = [f"[Search error: {e}]"]
        errors.append(f"Research failed for {top_domain}: {e}")

    return {"research_materials": materials, "errors": errors}


def debate_round1_node(state: DebateState) -> dict:
    """Round 1: Each expert provides initial statement."""
    from decision_prism.agents.expert import SMEExpertAgent
    from decision_prism.config import get_settings
    from decision_prism.llm.openrouter import OpenRouterProvider

    llm = OpenRouterProvider(
        api_key=get_settings().openrouter_api_key,
        model=get_settings().llm_model,
        base_url=get_settings().llm_base_url,
        temperature=get_settings().llm_temperature,
        max_tokens=get_settings().llm_max_tokens,
    )

    statements = []
    errors = []
    research_summary = "\n\n".join(
        content for contents in state["research_materials"].values() for content in contents
    )

    for expert in state["selected_experts"]:
        try:
            agent = SMEExpertAgent(domain=expert["domain"], stance=expert["stance"])
            content = _run(
                agent.run(
                    messages=[{"role": "user", "content": state["query"]}],
                    context={
                        "query": state["query"],
                        "research_summary": research_summary,
                    },
                    llm=llm,
                )
            )
            statements.append(
                {
                    "expert": expert["name"],
                    "domain": expert["domain"],
                    "stance": expert["stance"],
                    "content": content,
                }
            )
        except Exception as e:
            errors.append(f"Round 1 failed for {expert['name']}: {e}")

    return {"round_1_statements": statements, "current_round": 1, "errors": errors}


def debate_round2_node(state: DebateState) -> dict:
    """Round 2: Cross-examination between experts."""
    from decision_prism.agents.expert import SMEExpertAgent
    from decision_prism.config import get_settings
    from decision_prism.llm.openrouter import OpenRouterProvider

    llm = OpenRouterProvider(
        api_key=get_settings().openrouter_api_key,
        model=get_settings().llm_model,
        base_url=get_settings().llm_base_url,
        temperature=0.6,
        max_tokens=get_settings().llm_max_tokens,
    )

    challenges = []
    errors = []
    statements = state["round_1_statements"]

    for i, expert in enumerate(state["selected_experts"]):
        target_idx = (i + 1) % len(state["selected_experts"])
        if target_idx >= len(statements):
            continue

        target = state["selected_experts"][target_idx]
        target_statement = statements[target_idx]["content"]

        try:
            agent = SMEExpertAgent(domain=expert["domain"], stance=expert["stance"])
            challenge_msg = f"Challenge this statement:\n{target_statement}"
            challenge = _run(
                agent.run(
                    messages=[{"role": "user", "content": challenge_msg}],
                    context={"query": state["query"]},
                    llm=llm,
                )
            )
            target_agent = SMEExpertAgent(domain=target["domain"], stance=target["stance"])
            response = _run(
                target_agent.run(
                    messages=[
                        {"role": "user", "content": f"Respond to this challenge:\n{challenge}"}
                    ],
                    context={"query": state["query"]},
                    llm=llm,
                )
            )

            challenges.append(
                {
                    "challenger": expert["name"],
                    "target": target["name"],
                    "challenge": challenge,
                    "response": response,
                }
            )
        except Exception as e:
            errors.append(f"Round 2 challenge {i} failed: {e}")

    return {"round_2_challenges": challenges, "current_round": 2, "errors": errors}


def debate_round3_node(state: DebateState) -> dict:
    """Round 3: Risk assessment and expert revision."""
    from decision_prism.agents.expert import SMEExpertAgent
    from decision_prism.agents.risk import RiskAgent
    from decision_prism.config import get_settings
    from decision_prism.llm.openrouter import OpenRouterProvider

    llm = OpenRouterProvider(
        api_key=get_settings().openrouter_api_key,
        model=get_settings().llm_model,
        base_url=get_settings().llm_base_url,
        temperature=0.8,  # Higher for risk agent
        max_tokens=get_settings().llm_max_tokens,
    )

    errors = []
    risk_assessments = []

    debate_summary = "\n".join(
        f"[{s['expert']} ({s['stance']})]: {s['content'][:200]}..."
        for s in state["round_1_statements"]
    )

    risk_agent_agent = RiskAgent()
    try:
        risk_content = _run(
            risk_agent_agent.run(
                messages=[{"role": "user", "content": state["query"]}],
                context={
                    "query": state["query"],
                    "debate_summary": debate_summary,
                },
                llm=llm,
            )
        )
        risk_assessments.append(risk_content)
    except Exception as e:
        errors.append(f"Risk assessment failed: {e}")
        risk_content = "[Risk assessment failed]"

    revisions = []
    for expert in state["selected_experts"]:
        try:
            agent = SMEExpertAgent(domain=expert["domain"], stance=expert["stance"])
            revision = _run(
                agent.run(
                    messages=[
                        {
                            "role": "user",
                            "content": f"Revise position:\n{risk_content}",
                        }
                    ],
                    context={"query": state["query"]},
                    llm=OpenRouterProvider(
                        api_key=get_settings().openrouter_api_key,
                        model=get_settings().llm_model,
                        base_url=get_settings().llm_base_url,
                        temperature=0.5,  # More conservative for revision
                        max_tokens=get_settings().llm_max_tokens,
                    ),
                )
            )
            revisions.append(
                {
                    "expert": expert["name"],
                    "domain": expert["domain"],
                    "stance": expert["stance"],
                    "revision": revision,
                }
            )
        except Exception as e:
            errors.append(f"Round 3 revision failed for {expert['name']}: {e}")

    return {
        "round_3_revisions": revisions,
        "risk_assessments": risk_assessments,
        "current_round": 3,
        "errors": errors,
    }


def synthesize_report_node(state: DebateState) -> dict:
    """Synthesize all debate rounds into a structured report."""
    import json

    from decision_prism.agents.synthesizer import SynthesizerAgent
    from decision_prism.config import get_settings
    from decision_prism.llm.openrouter import OpenRouterProvider

    llm = OpenRouterProvider(
        api_key=get_settings().openrouter_api_key,
        model=get_settings().llm_model,
        base_url=get_settings().llm_base_url,
        temperature=0.3,  # Low for structured output
        max_tokens=get_settings().llm_max_tokens,
    )

    def _fmt_expert_n(s: dict) -> str:
        e = s["expert"]
        st = s["stance"]
        return f"[{e} ({st})]: {s['content']}"

    round_1_text = "\n".join(_fmt_expert_n(s) for s in state["round_1_statements"])

    def _fmt_challenge_n(c: dict) -> str:
        ch = c["challenge"]
        rs = c["response"]
        return f"[{c['challenger']} → {c['target']}]: Challenge: {ch}\nResponse: {rs}"

    round_2_text = "\n".join(_fmt_challenge_n(c) for c in state["round_2_challenges"])
    round_3_text = "\n".join(
        f"[{r['expert']} ({r['stance']}]): {r['revision']}" for r in state["round_3_revisions"]
    )
    risk_text = "\n".join(state["risk_assessments"])

    synthesizer = SynthesizerAgent()
    try:
        report_content = _run(
            synthesizer.run(
                messages=[{"role": "user", "content": state["query"]}],
                context={
                    "query": state["query"],
                    "round_1": round_1_text,
                    "round_2": round_2_text,
                    "round_3": round_3_text,
                    "risk_assessment": risk_text,
                },
                llm=llm,
            )
        )

        try:
            report_dict = json.loads(report_content)
        except json.JSONDecodeError:
            report_dict = {"raw_content": report_content, "parsing_error": True}
    except Exception as e:
        report_dict = {"error": str(e)}

    return {"report": report_dict}


def analysis_node(state: DebateState) -> dict:
    """Run Bayesian calibration and sentiment analysis."""
    from decision_prism.analysis.bayesian import monte_carlo_simulation
    from decision_prism.tools.sentiment import analyze_sentiment

    analysis_results: dict = {}
    errors = []

    report = state.get("report", {})
    conclusions = report.get("probability_conclusions", [])

    if conclusions:
        distributions = []
        for c in conclusions:
            prob = c.get("probability", 50)
            confidence = c.get("confidence", 30)
            claim = c.get("claim", "Unknown")
            low = max(0, prob - confidence)
            high = min(100, prob + confidence)
            distributions.append((claim, low, prob, high))

        if distributions:
            from decision_prism.config import get_settings

            mc_result = monte_carlo_simulation(
                distributions, get_settings().mc_simulations, get_settings().mc_seed
            )
            analysis_results["bayesian"] = mc_result

    research_materials = state.get("research_materials", {})
    if research_materials:
        all_content = [
            {"title": "", "url": "", "content": c}
            for contents in research_materials.values()
            for c in contents
        ]
        if all_content:
            sentiment = analyze_sentiment(all_content)
            analysis_results["sentiment"] = sentiment

    analysis_results["causal_chains"] = report.get("causal_chains", [])
    analysis_results["stakeholder_impact"] = report.get("stakeholder_impact", [])

    return {"final_analysis": analysis_results, "errors": errors}
