import streamlit as st
import numpy as np
import time

from ui.components import (
    apply_custom_css,
    render_header,
    render_disclaimer,
    render_pipeline_flow,
    plot_expected_vs_observed,
    plot_error_rate_gauge,
    plot_noise_vs_error_simulation,
    generate_report_json,
    generate_report_csv
)
from security.detector import (
    run_threat_verification_pipeline,
    clear_replay_ledger,
    get_session_ledger_size
)
from security.authorization import AUTHORIZED_VERIFIERS

# Set Streamlit page config
st.set_page_config(
    page_title="Quantum-Inspired QDS Threat Detection",
    page_icon="Ã¢Å¡â€ºÃ¯Â¸Â",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()
render_header()
render_disclaimer()

# Initialize session states for demo scenarios
if 'scenario' not in st.session_state:
    st.session_state['scenario'] = 'A. Legitimate Signature'
if 'sender' not in st.session_state:
    st.session_state['sender'] = 'ALICE'
if 'verifier' not in st.session_state:
    st.session_state['verifier'] = 'VERIFIER_A'
if 'message' not in st.session_state:
    st.session_state['message'] = 'PAY 5000 TO ALICE'
if 'num_measurements' not in st.session_state:
    st.session_state['num_measurements'] = 200
if 'noise' not in st.session_state:
    st.session_state['noise'] = 0.05
if 'threshold' not in st.session_state:
    st.session_state['threshold'] = 0.05

# Sidebar Controls
st.sidebar.markdown("## Ã¢Å¡â„¢Ã¯Â¸Â Simulation Parameters")

# 1-Click Demo Buttons
st.sidebar.markdown("### Ã°Å¸Å¡â‚¬ Demo Presets (1-Click)")
col_demo1, col_demo2 = st.sidebar.columns(2)

if col_demo1.button("Ã°Å¸Å¸Â¢ Legitimate"):
    st.session_state['scenario'] = 'A. Legitimate Signature'
    st.session_state['sender'] = 'ALICE'
    st.session_state['verifier'] = 'VERIFIER_A'
    st.session_state['noise'] = 0.02
    st.session_state['threshold'] = 0.05

if col_demo2.button("Ã°Å¸â€Â´ Forged"):
    st.session_state['scenario'] = 'B. Forged Signature'
    st.session_state['sender'] = 'ALICE'
    st.session_state['verifier'] = 'VERIFIER_A'

if col_demo1.button("Ã°Å¸â€˜Â¤ Impersonate"):
    st.session_state['scenario'] = 'C. Impersonation Attack'
    st.session_state['sender'] = 'EVE_MALICIOUS'
    st.session_state['verifier'] = 'VERIFIER_A'

if col_demo2.button("Ã°Å¸â€â€ž Replay"):
    st.session_state['scenario'] = 'D. Replay Attack'
    st.session_state['sender'] = 'ALICE'
    st.session_state['verifier'] = 'VERIFIER_A'

if col_demo1.button("Ã¢Å¡Â¡ Channel Noise"):
    st.session_state['scenario'] = 'E. Quantum Channel Manipulation'
    st.session_state['noise'] = 0.35

if col_demo2.button("Ã°Å¸Å¡Â« Unauthorized"):
    st.session_state['scenario'] = 'F. Unauthorized Verification'
    st.session_state['verifier'] = 'UNAUTHORIZED_EVE'

st.sidebar.markdown("---")

scenarios_list = [
    "A. Legitimate Signature",
    "B. Forged Signature",
    "C. Impersonation Attack",
    "D. Replay Attack",
    "E. Quantum Channel Manipulation",
    "F. Unauthorized Verification"
]

scenario_idx = scenarios_list.index(st.session_state['scenario']) if st.session_state['scenario'] in scenarios_list else 0

selected_scenario = st.sidebar.selectbox(
    "Attack Scenario",
    options=scenarios_list,
    index=scenario_idx
)
st.session_state['scenario'] = selected_scenario

sender_input = st.sidebar.text_input("Sender Identity", value=st.session_state['sender'])
st.session_state['sender'] = sender_input

verifier_options = AUTHORIZED_VERIFIERS + ["UNAUTHORIZED_EVE", "VERIFIER_MALICIOUS"]
verifier_idx = verifier_options.index(st.session_state['verifier']) if st.session_state['verifier'] in verifier_options else 0

verifier_input = st.sidebar.selectbox("Verifier Identity", options=verifier_options, index=verifier_idx)
st.session_state['verifier'] = verifier_input

message_input = st.sidebar.text_input("Message Payload", value=st.session_state['message'])
st.session_state['message'] = message_input

num_measurements = st.sidebar.slider("Number of Measurements", min_value=10, max_value=1000, value=st.session_state['num_measurements'], step=10)
st.session_state['num_measurements'] = num_measurements

channel_noise = st.sidebar.slider("Quantum Channel Noise Level", min_value=0.0, max_value=0.5, value=float(st.session_state['noise']), step=0.01)
st.session_state['noise'] = channel_noise

acceptance_threshold = st.sidebar.slider("Acceptance Error Threshold", min_value=0.01, max_value=0.20, value=float(st.session_state['threshold']), step=0.01)
st.session_state['threshold'] = acceptance_threshold

st.sidebar.markdown("---")
col_run, col_reset = st.sidebar.columns(2)
run_btn = col_run.button("Ã¢â€“Â¶ Run Pipeline", type="primary", use_container_width=True)

if col_reset.button("Ã°Å¸â€”â€˜ Reset Ledger", use_container_width=True):
    clear_replay_ledger()
    st.sidebar.success("Replay Ledger Cleared!")

# Input Validation
if not message_input.strip():
    st.error("Message payload cannot be empty. Please enter a message.")
    st.stop()

# Pipeline Execution
with st.spinner("Executing Quantum Teleportation & Threat Detection Pipeline..."):
    scenario_code = selected_scenario.split(".")[0].strip()
    report = run_threat_verification_pipeline(
        message=message_input,
        sender=sender_input,
        verifier=verifier_input,
        scenario=scenario_code,
        num_measurements=num_measurements,
        channel_noise=channel_noise,
        acceptance_threshold=acceptance_threshold,
        seed=42 if "Legitimate" in selected_scenario or "Forged" in selected_scenario else None
    )

# Render Visual Pipeline Header
render_pipeline_flow("DECISION")

# Prominent Verdict Banner
is_accepted = (report["decision"] == "VERIFICATION ACCEPTED")

if is_accepted:
    st.markdown(f'''
    <div class="status-accepted">
        Ã¢Å“â€¦ VERIFICATION ACCEPTED Ã¢â‚¬â€ LEGITIMATE QUANTUM DIGITAL SIGNATURE
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown(f'''
    <div class="status-threat">
        Ã°Å¸Å¡Â¨ THREAT DETECTED Ã¢â‚¬â€ {report["threat_type"].upper()}
    </div>
    ''', unsafe_allow_html=True)

# Metric Summary Cards
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric("Empirical Error Rate", f"{report['metrics']['error_rate']*100:.2f}%", f"Threshold: {acceptance_threshold*100:.1f}%")
col_m2.metric("Forgery Probability", f"{report['metrics']['forgery_probability']*100:.2f}%")
col_m3.metric("Verification Accuracy", f"{report['metrics']['accuracy']*100:.1f}%")
col_m4.metric("Replay Detected?", "YES Ã°Å¸Å¡Â¨" if report['replay_status']['replay_detected'] else "NO Ã¢Å“â€¦")
col_m5.metric("Authorized Verifier?", "YES Ã¢Å“â€¦" if report['authorized_verifier'] else "NO Ã°Å¸Å¡Â«")

# Tabbed Layout for Detailed Breakdown
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Ã°Å¸â€œÅ  Threat Dashboard",
    "Ã°Å¸â€â€˜ Signature Metadata",
    "Ã°Å¸Å’â‚¬ Quantum Teleportation",
    "Ã°Å¸â€œË† Measurement Analytics",
    "Ã°Å¸â€œËœ Security Interpretation",
    "Ã°Å¸â€œÂ¥ Audit Export"
])

with tab1:
    st.markdown("### Ã°Å¸â€ºÂ¡Ã¯Â¸Â Cyber Threat Analysis Summary")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown(f"**Target Message:** {report['message']}")
        st.markdown(f"**Claimed Sender:** <span class='mono-badge'>{report['sender_identity']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Verifier:** <span class='mono-badge'>{report['verifier_identity']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Attack Mode:** {report['threat_type']}")
        st.markdown(f"**Risk Severity:** **{report['risk_level']}**")
        st.markdown("</div>", unsafe_allow_html=True)

        fig_gauge = plot_error_rate_gauge(report['metrics']['error_rate'], acceptance_threshold)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with c2:
        fig_obs = plot_expected_vs_observed(report['measurement_data'])
        st.plotly_chart(fig_obs, use_container_width=True)

with tab2:
    st.markdown("### Ã°Å¸â€Â Signature Package & Dual-Layer Verification")
    st.markdown("""
    A Quantum Digital Signature (QDS) combines a **Classical Integrity Layer** (SHA-256 Digest) 
    with a **Simulated Quantum State Sequence** (Pauli eigenstates).
    """)
    sig = report['signature']
    st.json({
        "signature_id": sig['signature_id'],
        "message_digest_sha256": sig['message_digest'],
        "nonce": sig['nonce'],
        "timestamp": sig['timestamp'],
        "quantum_state_tokens": sig['quantum_states'],
        "bases_used": sig['bases']
    })

with tab3:
    st.markdown("### Ã°Å¸Å’â‚¬ Quantum Teleportation & Pauli Correction Simulation")
    st.markdown("""
    **Teleportation Protocol Flow:**
    1. **Entanglement Preparation:** Sender & Receiver share Bell pair $\\|\\Phi^+\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$.
    2. **Bell State Measurement (BSM):** Sender performs BSM on unknown signature qubit $|\\psi\\rangle$ and EPR qubit.
    3. **Classical Feed-forward:** Sender transmits 2 classical measurement bits (, b_2$) to Receiver.
    4. **Pauli Unitary Correction:** Receiver applies operator ^{b_2} Z^{b_1}$ to reconstruct signature state.
    """)
    st.info(f"**Simulated Channel Noise Level:** {channel_noise*100:.1f}% bit/phase flip probability.")
    fig_noise = plot_noise_vs_error_simulation(channel_noise, report['metrics']['error_rate'])
    st.plotly_chart(fig_noise, use_container_width=True)

with tab4:
    st.markdown("### Ã°Å¸â€œË† Projective Measurement Analytics")
    mdata = report['measurement_data']
    col_a1, col_a2 = st.columns(2)
    col_a1.metric("Total Measurements (N)", mdata['total_measurements'])
    col_a1.metric("Matching Eigenstates", mdata['matches'])
    col_a2.metric("Mismatched Outcomes", mdata['mismatches'])
    col_a2.metric("Expected Eigenstate", mdata['expected_state'])

    st.markdown("#### Measurement Frequency Breakdown")
    st.write(mdata['counts'])

with tab5:
    st.markdown("### Ã°Å¸â€œËœ Security Interpretation & Viva Defense Notes")
    st.markdown(f"""
    **Why was this attempt classified as {report['decision']}?**

    1. **Forgery:** If an adversary tampers with the signature payload or basis choices, the prepared quantum state $|\\psi\\rangle$ fails to match the receiver's projective measurement basis. Measurement collapse onto orthogonal states produces high mismatch ($> 50\\%$ theoretical for random state guess).
    2. **Impersonation:** The sender identity <{report['sender_identity']}> is verified against the signature's underlying key/state derivation. An attacker who cannot generate the matching state sequence triggers state discrepancies.
    3. **Replay Attack:** In-memory ledger tracking detected nonce reuse for signature ID {sig['signature_id']} (Ledger active size: {get_session_ledger_size()} entries). Re-sent valid signatures are rejected.
    4. **Quantum Channel Manipulation:** Noise induces phase-flips ($) and bit-flips ($), increasing empirical error rate above the specified threshold ({acceptance_threshold*100:.1f}%).
    5. **Unauthorized Verifier:** Verifier <{report['verifier_identity']}> is validated against authorized list.
    """)

with tab6:
    st.markdown("### Ã°Å¸â€œÂ¥ Download Audit & Verification Reports")
    col_json, col_csv = st.columns(2)

    json_data = generate_report_json(report)
    col_json.download_button(
        label="Ã°Å¸â€œâ€ž Download Report (JSON)",
        data=json_data,
        file_name=f"qds_audit_{sig['signature_id']}.json",
        mime="application/json"
    )

    csv_data = generate_report_csv(report)
    col_csv.download_button(
        label="Ã°Å¸â€œÅ  Download Report (CSV)",
        data=csv_data,
        file_name=f"qds_audit_{sig['signature_id']}.csv",
        mime="text/csv"
    )