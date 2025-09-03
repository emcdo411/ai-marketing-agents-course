# build_router.py
"""
START -> router -> (BI|Product|Email|Analyst) -> END

Conditional edges based on intent with confidence fallback (< threshold -> Analyst).
"""
from typing import Dict, Any

from langgraph.graph import StateGraph, START, END

from router_state import RouterState
from router_node import router, CONF_THRESHOLD
from bi_node import bi_node
from product_node import product_node
from email_node import email_node
from analyst_node import analyst_node

def build_router_app():
    g = StateGraph(RouterState)

    # Nodes
    g.add_node("router", router)
    g.add_node("bi", bi_node)
    g.add_node("product", product_node)
    g.add_node("email", email_node)
    g.add_node("analyst", analyst_node)

    # Start -> Router
    g.add_edge(START, "router")

    # Conditional edges based on router output
    def to_bi(s: RouterState) -> bool:
        return s.get("intent") == "BI" and float(s.get("confidence", 0)) >= CONF_THRESHOLD

    def to_product(s: RouterState) -> bool:
        return s.get("intent") == "Product" and float(s.get("confidence", 0)) >= CONF_THRESHOLD

    def to_email(s: RouterState) -> bool:
        return s.get("intent") == "Email" and float(s.get("confidence", 0)) >= CONF_THRESHOLD

    def to_analyst(s: RouterState) -> bool:
        # low-confidence or explicit Analyst/Other
        return (float(s.get("confidence", 0)) < CONF_THRESHOLD) or (s.get("intent") in ["Analyst", "Other"])

    g.add_conditional_edges(
        "router",
        {to_bi: "bi", to_product: "product", to_email: "email", to_analyst: "analyst"}
    )

    # All leaves -> END
    g.add_edge("bi", END)
    g.add_edge("product", END)
    g.add_edge("email", END)
    g.add_edge("analyst", END)

    return g.compile()
