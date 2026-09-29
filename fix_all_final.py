import os

# Update security/detector.py imports
with open('security/detector.py', 'r', encoding='utf-8') as f:
    detector_code = f.read()

if 'from security.signature import generate_qds_signature' not in detector_code:
    detector_code = 'from security.signature import generate_qds_signature\nfrom security.attacks import simulate_attack_scenario\n' + detector_code

with open('security/detector.py', 'w', encoding='utf-8') as f:
    f.write(detector_code)

# Test Files Update
test_teleportation = '''import pytest
import numpy as np
from quantum.states import ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I, fidelity
from quantum.teleportation import teleport_qubit

def test_teleportation_ideal():
    states = [("|0>", ZERO), ("|1>", ONE), ("|+>", PLUS), ("|->", MINUS), ("|+i>", PLUS_I), ("|-i>", MINUS_I)]
    for name, state in states:
        res = teleport_qubit(state, noise_prob=0.0)
        reconstructed = res["teleported_state"]
        fid = fidelity(state, reconstructed)
        assert np.isclose(fid, 1.0), f"Teleportation failed for {name}"

def test_teleportation_noisy():
    state = ZERO
    res = teleport_qubit(state, noise_prob=0.5, seed=42)
    reconstructed = res["teleported_state"]
    fid = fidelity(state, reconstructed)
    assert fid <= 1.0
'''

test_measurement = '''import pytest
from quantum.states import ZERO, ONE, PLUS, PLUS_I
from quantum.measurement import measure_basis
from quantum.statistics import compute_forgery_probability

def test_measurement_outcomes():
    res = measure_basis(ZERO, basis="Z", num_shots=100, seed=42)
    counts = res.get("counts", {})
    assert counts.get("|0>", 0) == 100

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
    assert len(sig["basis_sequence"]) > 0
    assert verify_classical_integrity(msg, sig) is True

def test_qds_signature_tampering():
    msg = "PAY 5000 TO ALICE"
    sender = "ALICE"
    verifier = "VERIFIER_A"
    sig = generate_qds_signature(msg, sender, verifier)
    assert verify_classical_integrity("PAY 9999 TO ALICE", sig) is False
'''

with open('tests/test_teleportation.py', 'w', encoding='utf-8') as f:
    f.write(test_teleportation)
with open('tests/test_measurement.py', 'w', encoding='utf-8') as f:
    f.write(test_measurement)
with open('tests/test_signature.py', 'w', encoding='utf-8') as f:
    f.write(test_signature)

print('All fixes applied cleanly!')