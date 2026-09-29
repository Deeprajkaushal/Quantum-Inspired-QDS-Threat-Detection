import os

test_states = '''import pytest
import numpy as np
from quantum.states import (
    KET_0, KET_1, KET_PLUS, KET_MINUS, KET_PLUS_I, KET_MINUS_I,
    normalize_state, state_fidelity, get_state_vector
)
from quantum.gates import I, X, Y, Z, H, S, tensor_product

def test_pauli_eigenstates_normalization():
    for name, state in [("|0>", KET_0), ("|1>", KET_1), ("|+>", KET_PLUS), ("|->", KET_MINUS), ("|+i>", KET_PLUS_I), ("|-i>", KET_MINUS_I)]:
        norm = np.linalg.norm(state)
        assert np.isclose(norm, 1.0), f"State {name} is not normalized"

def test_state_fidelity():
    assert np.isclose(state_fidelity(KET_0, KET_0), 1.0)
    assert np.isclose(state_fidelity(KET_0, KET_1), 0.0)
    assert np.isclose(state_fidelity(KET_PLUS, KET_MINUS), 0.0)
    assert np.isclose(state_fidelity(KET_0, KET_PLUS), 0.5)

def test_pauli_operators():
    assert np.allclose(X @ KET_0, KET_1)
    assert np.allclose(X @ KET_1, KET_0)
    assert np.allclose(Z @ KET_0, KET_0)
    assert np.allclose(Z @ KET_1, -KET_1)
    assert np.allclose(H @ KET_0, KET_PLUS)
    assert np.allclose(H @ KET_1, KET_MINUS)

def test_tensor_product():
    k00 = tensor_product(KET_0, KET_0)
    assert k00.shape == (4, 1)
    assert np.allclose(k00, np.array([[1], [0], [0], [0]]))
'''

test_teleportation = '''import pytest
import numpy as np
from quantum.states import KET_0, KET_1, KET_PLUS, KET_MINUS, KET_PLUS_I, KET_MINUS_I, state_fidelity
from quantum.bell import create_bell_pair
from quantum.teleportation import simulate_teleportation_pipeline

def test_teleportation_ideal():
    for name, state in [("|0>", KET_0), ("|1>", KET_1), ("|+>", KET_PLUS), ("|->", KET_MINUS), ("|+i>", KET_PLUS_I), ("|-i>", KET_MINUS_I)]:
        res = simulate_teleportation_pipeline(state, noise_level=0.0)
        reconstructed = res["reconstructed_state"]
        fidelity = state_fidelity(state, reconstructed)
        assert np.isclose(fidelity, 1.0), f"Teleportation failed for {name}"

def test_teleportation_noisy():
    state = KET_0
    res = simulate_teleportation_pipeline(state, noise_level=0.5, seed=42)
    reconstructed = res["reconstructed_state"]
    # With 50% noise, state fidelity will generally drop
    fidelity = state_fidelity(state, reconstructed)
    assert fidelity <= 1.0
'''

test_measurement = '''import pytest
from quantum.states import KET_0, KET_1, KET_PLUS, KET_PLUS_I
from quantum.measurement import perform_projective_measurement, measure_sequence
from quantum.statistics import calculate_empirical_error, compute_forgery_probability

def test_measurement_outcomes():
    # Measuring |0> in Z basis 100 times should yield |0> 100 times
    res = perform_projective_measurement(KET_0, basis="Z", num_measurements=100, seed=42)
    assert res["counts"]["|0>"] == 100
    assert res["counts"]["|1>"] == 0

def test_statistics_calculation():
    # Expected |0>, observed 90 |0> and 10 |1>
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
from security.signature import generate_qds_signature, verify_signature_integrity

def test_qds_signature_generation():
    msg = "PAY 5000 TO ALICE"
    sender = "ALICE"
    sig = generate_qds_signature(msg, sender, num_states=8)
    
    assert sig["sender"] == "ALICE"
    assert len(sig["quantum_states"]) == 8
    assert len(sig["bases"]) == 8
    assert verify_signature_integrity(msg, sig) is True

def test_qds_signature_tampering():
    msg = "PAY 5000 TO ALICE"
    sender = "ALICE"
    sig = generate_qds_signature(msg, sender, num_states=8)
    
    # Verify tampered message fails integrity
    assert verify_signature_integrity("PAY 9999 TO ALICE", sig) is False
'''

test_attacks = '''import pytest
from security.attacks import (
    simulate_legitimate_scenario,
    simulate_forged_scenario,
    simulate_impersonation_scenario,
    simulate_replay_scenario,
    simulate_channel_attack_scenario,
    simulate_unauthorized_verifier_scenario
)
from security.detector import run_threat_verification_pipeline, clear_replay_ledger

def test_legitimate_scenario():
    report = simulate_legitimate_scenario()
    assert report["decision"] == "VERIFICATION ACCEPTED"
    assert report["threat_type"] == "None (Legitimate)"
    assert report["metrics"]["error_rate"] <= 0.05

def test_forged_scenario():
    report = simulate_forged_scenario()
    assert report["decision"] == "THREAT DETECTED"
    assert report["threat_type"] == "Forged Signature"
    assert report["metrics"]["error_rate"] > 0.05

def test_impersonation_scenario():
    report = simulate_impersonation_scenario()
    assert report["decision"] == "THREAT DETECTED"
    assert report["threat_type"] == "Sender Impersonation"

def test_replay_scenario():
    clear_replay_ledger()
    report1 = simulate_legitimate_scenario()
    assert report1["decision"] == "VERIFICATION ACCEPTED"
    
    # Second run with same nonce triggers replay detection
    report2 = simulate_replay_scenario()
    assert report2["decision"] == "THREAT DETECTED"
    assert report2["threat_type"] == "Replay Attack"
    assert report2["replay_status"]["replay_detected"] is True

def test_unauthorized_verifier_scenario():
    report = simulate_unauthorized_verifier_scenario()
    assert report["decision"] == "THREAT DETECTED"
    assert report["threat_type"] == "Unauthorized Verification"
    assert report["authorized_verifier"] is False
'''

os.makedirs('tests', exist_ok=True)
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

print('All pytest test files created successfully!')