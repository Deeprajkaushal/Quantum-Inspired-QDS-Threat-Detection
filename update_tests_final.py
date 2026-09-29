import os

test_states = '''import pytest
import numpy as np
from quantum.states import (
    ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I,
    normalize, fidelity
)
from quantum.gates import I, X, Y, Z, H, S, tensor_product

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
    assert np.allclose(X @ ZERO, ONE)
    assert np.allclose(X @ ONE, ZERO)
    assert np.allclose(Z @ ZERO, ZERO)
    assert np.allclose(Z @ ONE, -ONE)
    assert np.allclose(H @ ZERO, PLUS)
    assert np.allclose(H @ ONE, MINUS)

def test_tensor_product():
    k00 = tensor_product(ZERO, ZERO)
    assert k00.shape == (4, 1)
    assert np.allclose(k00, np.array([[1], [0], [0], [0]]))
'''

test_teleportation = '''import pytest
import numpy as np
from quantum.states import ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I, fidelity
from quantum.teleportation import simulate_teleportation_pipeline

def test_teleportation_ideal():
    states = [("|0>", ZERO), ("|1>", ONE), ("|+>", PLUS), ("|->", MINUS), ("|+i>", PLUS_I), ("|-i>", MINUS_I)]
    for name, state in states:
        res = simulate_teleportation_pipeline(state, noise_level=0.0)
        reconstructed = res["reconstructed_state"]
        fid = fidelity(state, reconstructed)
        assert np.isclose(fid, 1.0), f"Teleportation failed for {name}"

def test_teleportation_noisy():
    state = ZERO
    res = simulate_teleportation_pipeline(state, noise_level=0.5, seed=42)
    reconstructed = res["reconstructed_state"]
    fid = fidelity(state, reconstructed)
    assert fid <= 1.0
'''

test_measurement = '''import pytest
from quantum.states import ZERO, ONE, PLUS, PLUS_I
from quantum.measurement import perform_projective_measurement
from quantum.statistics import calculate_empirical_error, compute_forgery_probability

def test_measurement_outcomes():
    res = perform_projective_measurement(ZERO, basis="Z", num_measurements=100, seed=42)
    assert res["counts"]["|0>"] == 100
    assert res["counts"]["|1>"] == 0

def test_statistics_calculation():
    stats = calculate_empirical_error(["|0>"]*90 + ["|1>"]*10, expected_eigenstate="|0>")
    assert stats["matches"] == 90
    assert stats["mismatches"] == 10
    assert stats["error_rate"] == 0.10
    assert stats["total_measurements"] == 100

def test_forgery_probability():
    prob_low = compute_forgery_probability(error_rate=0.01, num_measurements=200)
    prob_high = compute_forgery_probability(error_rate=0.50, num_measurements=200)
    assert prob_low < prob_high
    assert prob_high > 0.95
'''

test_signature = '''import pytest
from security.signature import generate_qds_signature, verify_classical_integrity

def test_qds_signature_generation():
    msg = "PAY 5000 TO ALICE"
    sender = "ALICE"
    sig = generate_qds_signature(msg, sender, num_states=8)
    
    assert sig["sender"] == "ALICE"
    assert len(sig["quantum_states"]) == 8
    assert len(sig["bases"]) == 8
    assert verify_classical_integrity(msg, sig) is True

def test_qds_signature_tampering():
    msg = "PAY 5000 TO ALICE"
    sender = "ALICE"
    sig = generate_qds_signature(msg, sender, num_states=8)
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
    assert report["metrics"]["error_rate"] > 0.05

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
    assert report2["replay_status"]["replay_detected"] is True

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

print('Updated tests final!')