import streamlit as st
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

def render_risk_gauge(score: float, label: str, color: str):
    """Renders a risk gauge using Plotly."""
    fig = px.pie(
        values=[score, 10-score],
        names=["Risk", "Safety"],
        hole=0.7,
        color_discrete_sequence=[color, "#f0f0f0"]
    )
    fig.update_traces(textinfo='none', hoverinfo='none')
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=200,
        annotations=[dict(text=f"{score}/10<br>{label}", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)

def render_clause_card(clause: Dict[str, Any], index: int):
    """Renders a single clause analysis card."""
    with st.expander(f"Clause {index}: {clause['header'][:100]}...", expanded=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Category:** {clause['category']}")
            st.markdown(f"**Explanation:** {clause['explanation']}")
            
            if clause.get("detected_risks"):
                st.markdown("**Detected Risks:**")
                for risk in clause["detected_risks"]:
                    st.warning(risk)
                    
            if clause.get("ambiguities"):
                st.markdown("**Ambiguities Found:**")
                for amb in clause["ambiguities"]:
                    st.info(f"Term: '{amb['term']}' - {amb['reason']}")
        
        with col2:
            st.markdown(f"<h3 style='color:{clause['risk_color']}'>{clause['risk_label']}</h3>", unsafe_allow_html=True)
            st.metric("Risk Score", f"{clause['risk_score']}/10")
            
        # Alternative Suggestion
        if clause.get("alternative"):
            st.markdown("---")
            st.markdown("**💡 SME-Friendly Alternative:**")
            st.success(clause["alternative"])
            st.info(f"*Rationale:* {clause['alternative_explanation']}")

def render_entity_summary(entities: Dict[str, Any]):
    """Renders the extracted entities summary."""
    st.subheader("📌 Key Entities & Terms")
    
    struct = entities.get("structured_data", {})
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown("**Parties**")
        parties = struct.get("Parties", [])
        if isinstance(parties, list):
            for p in parties: st.write(f"- {p}")
        else: st.write(parties)
        
    with cols[1]:
        st.markdown("**Timeline**")
        st.write(f"Effective Date: {struct.get('Effective Date', 'N/A')}")
        st.write(f"Notice Period: {struct.get('Termination Notice Period', 'N/A')}")
        
    with cols[2]:
        st.markdown("**Jurisdiction**")
        st.write(struct.get("Governing Law/Jurisdiction", "N/A"))
