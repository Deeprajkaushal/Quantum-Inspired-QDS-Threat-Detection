# Presentation Talking Points & Script

## Overview
**Project Title:** Quantum-Inspired Cyber Threat Detection Framework for Teleportation-Based Quantum Digital Signatures (QDS)  
**Speaker Duration:** 2?3 minutes  

---

## Slide 1: Title & Introduction
**Speaker Script:**  
"Good morning honorable judges and faculty members. Today I am presenting our software framework: *Quantum-Inspired Cyber Threat Detection for Teleportation-Based Quantum Digital Signatures*. 
As quantum computing advances, classical asymmetric cryptography faces existential vulnerabilities. Our system models a teleportation-based Quantum Digital Signature pipeline and uses statistical threat detection rules to identify signature forgery, sender impersonation, replay attacks, channel noise, and unauthorized verification attempts in real-time."

---

## Slide 2: Problem & Motivation
**Speaker Script:**  
"Shor's algorithm running on a sufficiently large quantum computer will easily break RSA and Elliptic Curve signatures by solving integer factorization and discrete logarithms in polynomial time. Quantum Digital Signatures leverage quantum mechanical principles to achieve physical information-theoretic security. However, implementing and testing QDS protocols requires demonstrable simulation frameworks to evaluate how quantum channel disturbances and cyber attack vectors behave under measurement statistics."

---

## Slide 3: Proposed Framework Architecture
**Speaker Script:**  
"Our framework employs a dual-layer security approach:
1. A **Classical Integrity Layer** that computes SHA-256 message digests, tracks session nonces, and validates sender identities.
2. A **Simulated Quantum Signature Layer** composed of sequences of Pauli eigenstates (|0>, |1>, |+>, |->, |+i>, |-i>).
Quantum signature verification is simulated via quantum teleportation with Bell state measurement and feedforward Pauli corrections."

---

## Slide 4: Quantum Mechanics & Teleportation Model
**Speaker Script:**  
"The core quantum simulation relies on transparent linear algebra using NumPy:
- We prepare maximally entangled Bell pairs |Phi+> = 1/sqrt(2)(|00> + |11>).
- Sender Alice performs a Bell State Measurement on her signature qubit and her half of the EPR pair.
- The resulting 2 classical bits are transmitted to Bob, who applies the corresponding Pauli correction operator (Identity, X, Z, or ZX) to reconstruct Alice's original state.
- Receiver Bob then performs projective measurements across X, Y, and Z bases to compute empirical state overlap."

---

## Slide 5: Threat Detection & Attack Vector Modes
**Speaker Script:**  
"Our application models six distinct security scenarios:
1. **Legitimate Signature:** Verified state match within threshold.
2. **Signature Forgery:** Altered states or tampered message content trigger high error rates (>50%).
3. **Sender Impersonation:** Rejects unauthorized key derivation and invalid digests.
4. **Replay Attack:** Tracked in-memory session ledger flags reused signature nonces.
5. **Channel Manipulation:** Evaluates environmental noise and bit/phase flip rates against threshold.
6. **Unauthorized Verifier:** Validates verifier identity against authorized access lists."

---

## Slide 6: Prototype & Empirical Results
**Speaker Script:**  
"As shown in our live Streamlit application, the statistical engine computes empirical error rates, estimated forgery probabilities, and verification accuracy. Our 1-click demo preset buttons allow judges to test all six attack vectors in under 2 minutes with deterministic, reproducible outcomes."

---

## Slide 7: Impact, Limitations & Future Scope
**Speaker Script:**  
"In conclusion, this project provides a clear academic tool for studying post-quantum signature threat dynamics. We explicitly clarify that this is a classical software simulation on NumPy. Future work includes integrating physical QKD backends such as IBM Qiskit and optical channel simulators. Thank you!"
