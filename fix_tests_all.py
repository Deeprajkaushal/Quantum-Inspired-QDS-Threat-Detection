import os

test_states = '''import pytest
import numpy as np
from quantum.states import (
    ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I,
    normalize, fidelity
)
from quantum.gates import I_GATE, X_GATE, Y_GATE, Z_GATE, H_GATE, S_GATE, tensor_product

def test_pauli_eigenstates_normalization():
    states = [("|0>", ZERO), ("|1>", ONE), ("|+>", PLUS), ("|->", MINUS), ("|+i>", PLUS_I), ("|-i>", MINUS_I)]
    for name, state in states:
        norm = np.linalg.norm(state)
        assert np.isclose(norm, 1.0), f"State {name} is not normalized"

def test_state_fidelity():
    assert np.isclose(fidelity(ZERO, ZERO), 1.0)
    assert np.isclose(fidelity(ZERO, ONE), 0.0)
    assert np.isclose(fidelity(PLUS, MINUS), 0.0)
    assert np.isclose(fidelity(ZERO, PLUS), 0.5)

def test_pauli_operators():
    assert np.allclose(X_GATE @ ZERO, ONE)
    assert np.allclose(X_GATE @ ONE, ZERO)
    assert np.allclose(Z_GATE @ ZERO, ZERO)
    assert np.allclose(Z_GATE @ ONE, -ONE)
    assert np.allclose(H_GATE @ ZERO, PLUS)
    assert np.allclose(H_GATE @ ONE, MINUS)

def test_tensor_product():
    k00 = tensor_product(ZERO, ZERO)
    assert k00.shape == (4,)
    assert np.allclose(k00, np.array([1, 0, 0, 0]))
'''

test_teleportation = '''import pytest
import numpy as np
from quantum.states import ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I, fidelity
from quantum.teleportation import teleport_qubit

def test_teleportation_ideal():
    states = [("|0>", ZERO), ("|1>", ONE), ("|+>", PLUS), ("|->", MINUS), ("|+i>", PLUS_I), ("|-i>", MINUS_I)]
    for name, state in states:
        res = teleport_qubit(state, noise_prob=0.0)
        reconstructed = res["received_state"]
        fid = fidelity(state, reconstructed)
        assert np.isclose(fid, 1.0), f"Teleportation failed for {name}"

def test_teleportation_noisy():
    state = ZERO
    res = teleport_qubit(state, noise_prob=0.5, seed=42)
    reconstructed = res["received_state"]
    fid = fidelity(state, reconstructed)
    assert fid <= 1.0
'''

test_measurement = '''import pytest
from quantum.states import ZERO, ONE, PLUS, PLUS_I
from quantum.measurement import measure_basis
from quantum.statistics import calculate_verification_stats, compute_forgery_probability

def test_measurement_outcomes():
    res = measure_basis(ZERO, basis="Z", num_shots=100, seed=42)
    counts = res.get("counts", {})
    assert counts.get("|0>", 0) == 100

def test_statistics_calculation():
    stats = calculate_verification_stats(["|0>"]*10, ["|0>"]*9 + ["|1>"]*1)
    assert stats["matches"] == 9
    assert stats["mismatches"] == 1
    assert stats["error_rate"] == 0.10

def test_forgery_probability():
    prob_low = compute_forgery_probability(error_rate=0.01, num_measurements=200)
    prob_high = compute_forgery_probability(error_rate=0.50, num_measurements=200)
    assert prob_low < prob_high
'''

test_signature = '''import pytest
from security.signature import generate_qds_signature, verify_classical_integrity

def test_qds_signature_generation():
    msg = "PAY 5000 TO ALICE"
    sender = "ALICE"
    verifier = "VERIFIER_A"
    sig = generate_qds_signature(msg, sender, verifier)
    
    assert sig["sender_id"] == "ALICE"
    assert len(sig["quantum_states"]) > 0
    assert len(sig["bases"]) > 0
    assert verify_classical_integrity(msg, sig) is True

def test_qds_signature_tampering():
    msg = "PAY 5000 TO ALICE"
    sender = "ALICE"
    verifier = "VERIFIER_A"
    sig = generate_qds_signature(msg, sender, verifier)
    assert verify_classical_integrity("PAY 9999 TO ALICE", sig) is False
'''

test_attacks = '''import pytest
from security.detector import run_threat_verification_pipeline, clear_replay_ledger

def test_legitimate_scenario():
    report = run_threat_verification_pipeline(
        message="PAY 5000 TO ALICE",
        sender="ALICE",
        verifier="VERIFIER_A",
        scenario="A",
        num_measurements=200,
        channel_noise=0.02,
        acceptance_threshold=0.05,
        seed=42
    )
    assert report["decision"] == "VERIFICATION ACCEPTED"
    assert report["threat_type"] == "None (Legitimate)"
    assert report["metrics"]["error_rate"] <= 0.05

def test_forged_scenario():
    report = run_threat_verification_pipeline(
        message="PAY 5000 TO ALICE",
        sender="ALICE",
        verifier="VERIFIER_A",
        scenario="B",
        num_measurements=200,
        channel_noise=0.02,
        acceptance_threshold=0.05,
        seed=42
    )
    assert report["decision"] == "THREAT DETECTED"
    assert report["threat_type"] == "Forged Signature"

def test_impersonation_scenario():
    report = run_threat_verification_pipeline(
        message="PAY 5000 TO ALICE",
        sender="EVE_MALICIOUS",
        verifier="VERIFIER_A",
        scenario="C",
        num_measurements=200,
        channel_noise=0.02,
        acceptance_threshold=0.05
    )
    assert report["decision"] == "THREAT DETECTED"
    assert report["threat_type"] == "Sender Impersonation"

def test_replay_scenario():
    clear_replay_ledger()
    report1 = run_threat_verification_pipeline(
        message="PAY 5000 TO ALICE",
        sender="ALICE",
        verifier="VERIFIER_A",
        scenario="A",
        seed=100
    )
    assert report1["decision"] == "VERIFICATION ACCEPTED"
    
    report2 = run_threat_verification_pipeline(
        message="PAY 5000 TO ALICE",
        sender="ALICE",
        verifier="VERIFIER_A",
        scenario="D",
        seed=100
    )
    assert report2["decision"] == "THREAT DETECTED"
    assert report2["threat_type"] == "Replay Attack"

def test_unauthorized_verifier_scenario():
    report = run_threat_verification_pipeline(
        message="PAY 5000 TO ALICE",
        sender="ALICE",
        verifier="UNAUTHORIZED_EVE",
        scenario="F"
    )
    assert report["decision"] == "THREAT DETECTED"
    assert report["threat_type"] == "Unauthorized Verification"
    assert report["authorized_verifier"] is False
'''

with open('tests/test_states.py', 'w', encoding='utf-8') as f:
    f.write(test_states)
with open('tests/test_teleportation.py', 'w', encoding='utf-8') as f:
    f.write(test_teleportation)
with open('tests/test_measurement.py', 'w', encoding='utf-8') as f:
    f.write(test_measurement)
with open('tests/test_signature.py', 'w', encoding='utf-8') as f:
    f.write(test_signature)
with open('tests/test_attacks.py', 'w', encoding='utf-8') as f:
    f.write(test_attacks)

print('Rewrite tests clean!')