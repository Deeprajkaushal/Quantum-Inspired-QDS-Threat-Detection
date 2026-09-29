import pytest
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
