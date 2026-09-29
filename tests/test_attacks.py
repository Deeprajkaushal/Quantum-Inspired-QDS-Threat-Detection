import pytest
from security.detector import run_threat_verification_pipeline, clear_replay_ledger

def test_legitimate_scenario():
    report = run_threat_verification_pipeline(
        message='PAY 5000 TO ALICE',
        sender='ALICE',
        verifier='VERIFIER_A',
        scenario='A',
        num_measurements=200,
        channel_noise=0.02,
        acceptance_threshold=0.05,
        seed=42
    )
    assert report['decision'] == 'VERIFICATION ACCEPTED'
    assert report['metrics']['error_rate'] <= 0.05

def test_forged_scenario():
    report = run_threat_verification_pipeline(
        message='PAY 5000 TO ALICE',
        sender='ALICE',
        verifier='VERIFIER_A',
        scenario='B',
        num_measurements=200,
        channel_noise=0.02,
        acceptance_threshold=0.05,
        seed=42
    )
    assert report['decision'] == 'THREAT DETECTED'

def test_impersonation_scenario():
    report = run_threat_verification_pipeline(
        message='PAY 5000 TO ALICE',
        sender='EVE_MALICIOUS',
        verifier='VERIFIER_A',
        scenario='C',
        num_measurements=200,
        channel_noise=0.02,
        acceptance_threshold=0.05
    )
    assert report['decision'] == 'THREAT DETECTED'

def test_replay_scenario():
    clear_replay_ledger()
    report1 = run_threat_verification_pipeline(
        message='PAY 5000 TO ALICE',
        sender='ALICE',
        verifier='VERIFIER_A',
        scenario='A',
        seed=100
    )
    assert report1['decision'] == 'VERIFICATION ACCEPTED'
    
    report2 = run_threat_verification_pipeline(
        message='PAY 5000 TO ALICE',
        sender='ALICE',
        verifier='VERIFIER_A',
        scenario='D',
        seed=100
    )
    assert report2['decision'] == 'THREAT DETECTED'

def test_unauthorized_verifier_scenario():
    report = run_threat_verification_pipeline(
        message='PAY 5000 TO ALICE',
        sender='ALICE',
        verifier='UNAUTHORIZED_EVE',
        scenario='F'
    )
    assert report['decision'] == 'THREAT DETECTED'
    assert report['authorized_verifier'] is False
