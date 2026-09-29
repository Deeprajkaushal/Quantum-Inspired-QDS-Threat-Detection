import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0d1322 100%);
        color: #e5e7eb;
    }
    
    .cyber-header {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .cyber-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60a5fa, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .cyber-subtitle {
        font-size: 1.05rem;
        color: #9ca3af;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .quantum-card {
        background: rgba(31, 41, 55, 0.6);
        border: 1px solid rgba(75, 85, 99, 0.4);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        backdrop-filter: blur(8px);
    }
    
    .status-accepted {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        border-left: 6px solid #10b981;
        color: #34d399;
        padding: 1.25rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }

    .status-threat {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        border-left: 6px solid #ef4444;
        color: #f87171;
        padding: 1.25rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
    }
    
    .status-ready {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid #3b82f6;
        border-left: 6px solid #3b82f6;
        color: #60a5fa;
        padding: 1.25rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
    }
    
    .pipeline-step {
        display: inline-block;
        background: #1f2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        font-size: 0.82rem;
        font-weight: 600;
        color: #9ca3af;
        text-align: center;
    }

    .pipeline-step.active {
        border-color: #8b5cf6;
        color: #c084fc;
        background: rgba(139, 92, 246, 0.15);
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.3);
    }
    
    .mono-badge {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid #374151;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        color: #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class="cyber-header">
        <div class="cyber-title">⚛️ Quantum-Inspired Cyber Threat Detection</div>
        <div class="cyber-subtitle">Teleportation-Based Quantum Digital Signature (QDS) Verification Simulator</div>
    </div>
    """, unsafe_allow_html=True)

def render_disclaimer():
    st.warning(
        "**SOFTWARE SIMULATION & QUANTUM-INSPIRED FRAMEWORK NOTICE:** "
        "This application simulates quantum state dynamics (Bell states, teleportation, measurement statistics) using classical software (NumPy). "
        "It does not execute on physical quantum hardware nor provide physical information-theoretic security bounds in real-time."
    )

def render_pipeline_flow(current_step="DECISION"):
    steps = [
        ("1. MESSAGE", "MESSAGE"),
        ("2. QDS SIGN", "SIGN"),
        ("3. BELL PAIR", "ENTANGLEMENT"),
        ("4. TELEPORT", "TELEPORT"),
        ("5. PAULI CORR", "PAULI"),
        ("6. MEASURE", "MEASUREMENT"),
        ("7. STATS", "STATS"),
        ("8. THRESHOLD", "DECISION")
    ]
    
    html = "<div style='display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: center; margin-bottom: 20px;'>"
    for idx, (label, key) in enumerate(steps):
        active_class = "active" if key == current_step or current_step == "ALL" else ""
        html += f"<div class='pipeline-step {active_class}'>{label}</div>"
        if idx < len(steps) - 1:
            html += "<span style='color: #4b5563;'>➔</span>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def plot_expected_vs_observed(measurement_data):
    counts = measurement_data.get("counts", {})
    expected = measurement_data.get("expected_state", "|0>")
    
    states = ["|0>", "|1>", "|+>", "|->", "|+i>", "|-i>"]
    observed_counts = [counts.get(s, 0) for s in states]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=states,
        y=observed_counts,
        marker_color=['#10b981' if s == expected else '#ef4444' for s in states],
        name="Observed Frequency"
    ))
    
    fig.update_layout(
        title="Measurement Outcome Distribution (Bases: Z, X, Y)",
        xaxis_title="Measured Quantum State",
        yaxis_title="Count / Frequency",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        height=320,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def plot_error_rate_gauge(error_rate, threshold):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = float(error_rate * 100),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Empirical Error Rate (%)", 'font': {'size': 16, 'color': '#e5e7eb'}},
        delta = {'reference': float(threshold * 100), 'increasing': {'color': "#ef4444"}, 'decreasing': {'color': "#10b981"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#9ca3af"},
            'bar': {'color': "#3b82f6"},
            'bgcolor': "rgba(17,24,39,0.8)",
            'borderwidth': 2,
            'bordercolor': "#374151",
            'steps': [
                {'range': [0, threshold * 100], 'color': 'rgba(16, 185, 129, 0.2)'},
                {'range': [threshold * 100, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#f59e0b", 'width': 4},
                'thickness': 0.75,
                'value': float(threshold * 100)
            }
        }
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def plot_noise_vs_error_simulation(channel_noise_level, base_error):
    noise_levels = [i * 0.05 for i in range(21)]
    error_rates = [min(1.0, noise * 0.75 + base_error) for noise in noise_levels]
    
    fig = px.line(
        x=noise_levels,
        y=error_rates,
        labels={'x': 'Quantum Channel Noise Level', 'y': 'Simulated Error Rate'},
        title="Channel Disturbance Impact on QDS Error Rate"
    )
    fig.add_vline(x=channel_noise_level, line_dash="dash", line_color="#ec4899", annotation_text="Current Setting")
    fig.update_traces(line_color="#8b5cf6", line_width=3)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        height=300,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def generate_report_json(report_data):
    return json.dumps(report_data, indent=2)

def generate_report_csv(report_data):
    flattened = {
        "timestamp": report_data.get("timestamp", ""),
        "decision": report_data.get("decision", ""),
        "threat_type": report_data.get("threat_type", ""),
        "sender_identity": report_data.get("sender_identity", ""),
        "verifier_identity": report_data.get("verifier_identity", ""),
        "authorized_verifier": report_data.get("authorized_verifier", False),
        "message": report_data.get("message", ""),
        "digest_sha256": report_data.get("signature", {}).get("message_digest", ""),
        "error_rate": report_data.get("metrics", {}).get("error_rate", 0.0),
        "threshold": report_data.get("metrics", {}).get("threshold", 0.05),
        "forgery_probability": report_data.get("metrics", {}).get("forgery_probability", 0.0),
        "matches": report_data.get("metrics", {}).get("matches", 0),
        "total_measurements": report_data.get("metrics", {}).get("total_measurements", 0),
        "replay_detected": report_data.get("replay_status", {}).get("replay_detected", False)
    }
    df = pd.DataFrame([flattened])
    return df.to_csv(index=False)
