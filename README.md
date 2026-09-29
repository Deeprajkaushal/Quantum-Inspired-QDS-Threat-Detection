# Quantum-Inspired Cyber Threat Detection Framework for Teleportation-Based Quantum Digital Signatures

> **SOFTWARE SIMULATION NOTICE:** This project is a software-inspired simulation built with Python and NumPy to model quantum state verification and cyber threat detection against Quantum Digital Signatures (QDS). It runs on classical hardware and clearly distinguishes simulated quantum dynamics from physical quantum hardware.

---

## ?? Overview
This framework simulates a **Quantum Digital Signature (QDS)** verification pipeline based on:
- Bell-state entanglement ($|\Phi^+\rangle$)
- Quantum teleportation with classical feedforward
- Pauli unitary corrections ($I, X, Z, ZX$)
- Projective measurements across $X$, $Y$, and $Z$ bases
- Empirical error rate analysis and statistical threshold threat detection

---

## ??? Cyber Threat Modes Detected
1. **Signature Forgery:** Detects state/basis tampering and SHA-256 digest mismatches.
2. **Sender Impersonation:** Identifies unauthorized sender key mismatches.
3. **Replay Attack:** In-memory session ledger flags signature nonces submitted more than once.
4. **Quantum Channel Manipulation:** Measures bit-flip ($X$) and phase-flip ($Z$) noise disturbance.
5. **Unauthorized Verification Attempt:** Validates verifier identity against authorized list.

---

## ?? Quick Start & Installation

### Prerequisites
- Python 3.10+
- Windows / Linux / macOS

### Installation
```bash
# Clone repository
git clone https://github.com/USER/Quantum-Inspired-QDS-Threat-Detection.git
cd Quantum-Inspired-QDS-Threat-Detection

# Install dependencies
pip install -r requirements.txt
```

### Running the Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ?? Running Automated Tests
```bash
python -m pytest -v
```

---

## ?? Presentation & Documentation Assets
- **PowerPoint Presentation:** `presentation/QDS_Threat_Detection_Presentation.pptx`
- **Presentation Content Script:** `presentation/presentation_content.md`
- **Technical Report:** `docs/TECHNICAL_REPORT.md`
- **Security Model:** `docs/SECURITY_MODEL.md`
- **Architecture Guide:** `docs/ARCHITECTURE.md`

---

## ?? License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
