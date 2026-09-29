from security.signature import generate_qds_signature
from security.attacks import simulate_attack_scenario
import hashlib
import numpy as np
from quantum.states import name_to_state
from quantum.teleportation import teleport_qubit
from quantum.statistics import calculate_verification_stats
from security.authorization import VerifierAuthorization

class InMemReplayLedger:
    def __init__(self):
        self._consumed_ids = set()

    def is_consumed(self, signature_id: str) -> bool:
        return signature_id in self._consumed_ids

    def mark_consumed(self, signature_id: str):
        self._consumed_ids.add(signature_id)

    def reset(self):
        self._consumed_ids.clear()

SESSION_REPLAY_LEDGER = InMemReplayLedger()

class QDSThreatDetector:
    def __init__(self, verifier_auth: VerifierAuthorization = None):
        self.auth = verifier_auth or VerifierAuthorization()

    def verify_signature(
        self,
        signature: dict,
        verifier_id: str,
        num_shots: int = 500,
        acceptance_threshold: float = 0.15,
        noise_level: float = 0.0,
        force_replay: bool = False,
        ledger: InMemReplayLedger = SESSION_REPLAY_LEDGER
    ) -> dict:
        if not self.auth.is_authorized(verifier_id):
            return {
                'decision': 'THREAT DETECTED',
                'threat_type': 'UNAUTHORIZED VERIFICATION ATTEMPT',
                'risk_indicator': 'HIGH',
                'authorization_status': 'UNAUTHORIZED',
                'replay_status': 'NOT CHECKED',
                'classical_integrity': 'NOT CHECKED',
                'error_rate': 1.0,
                'threshold': acceptance_threshold,
                'forgery_probability': 1.0,
                'verification_accuracy': 0.0,
                'reason': f'Verifier {verifier_id} is not in the list of authorized verifiers.',
                'security_advice': 'Reject verification request immediately. Audit access control policy.',
                'teleportation_results': [],
                'stats': {}
            }

        sig_id = signature.get('signature_id', '')
        if force_replay or ledger.is_consumed(sig_id):
            return {
                'decision': 'THREAT DETECTED',
                'threat_type': 'REPLAY ATTACK DETECTED',
                'risk_indicator': 'HIGH',
                'authorization_status': 'AUTHORIZED',
                'replay_status': 'REPLAY_DETECTED',
                'classical_integrity': 'VALID',
                'error_rate': 1.0,
                'threshold': acceptance_threshold,
                'forgery_probability': 1.0,
                'verification_accuracy': 0.0,
                'reason': f'Signature ID {sig_id} or nonce has been previously consumed in this session.',
                'security_advice': 'Stale nonce or duplicate signature submitted. Reject to prevent replay exploits.',
                'teleportation_results': [],
                'stats': {}
            }

        computed_digest = hashlib.sha256(signature['message'].encode('utf-8')).hexdigest()
        digest_valid = (computed_digest == signature['message_digest'])
        classical_integrity = 'VALID' if digest_valid else 'TAMPERED'

        teleportation_results = []
        expected_states = signature['quantum_states']

        for idx, state_name in enumerate(expected_states):
            state_vec = name_to_state(state_name)
            tele_res = teleport_qubit(
                input_state=state_vec,
                noise_prob=noise_level,
                noise_type='depolarizing',
                seed=42 + idx
            )
            teleportation_results.append(tele_res)

        stats = calculate_verification_stats(expected_states, teleportation_results, num_shots_per_state=num_shots)
        empirical_error_rate = stats['empirical_error_rate']

        if not digest_valid:
            empirical_error_rate = max(empirical_error_rate, 0.45)
            stats['empirical_error_rate'] = empirical_error_rate
            stats['verification_accuracy'] = 1.0 - empirical_error_rate

        m_tokens = len(expected_states)
        base_guess_prob = (0.5 ** m_tokens)
        forgery_prob = min(1.0, max(0.0, 1.0 - (1.0 - base_guess_prob) * (1.0 - empirical_error_rate * 2.0)))

        is_accepted = (empirical_error_rate <= acceptance_threshold) and digest_valid

        if is_accepted:
            decision = 'VERIFICATION ACCEPTED'
            threat_type = 'NONE (LEGITIMATE)'
            risk_indicator = 'LOW'
            reason = 'Empirical error rate is within acceptable noise threshold. Signature verified.'
            security_advice = 'Signature is authentic. Teleportation measurements match expected Pauli eigenstates.'
            ledger.mark_consumed(sig_id)
        else:
            decision = 'THREAT DETECTED'
            risk_indicator = 'HIGH'
            if not digest_valid:
                threat_type = 'FORGED SIGNATURE (CLASSICAL TAMPERING)'
                reason = 'Classical SHA-256 message digest does not match signature metadata.'
                security_advice = 'Message text was tampered with post-signing.'
            elif noise_level > 0 and empirical_error_rate > acceptance_threshold:
                threat_type = 'QUANTUM CHANNEL MANIPULATION / NOISE'
                reason = f'Channel noise rate ({noise_level:.2f}) produced measurement error ({empirical_error_rate:.4f}) exceeding threshold ({acceptance_threshold:.2f}).'
                security_advice = 'High channel disturbance detected. Eavesdropping or physical noise suspected.'
            else:
                threat_type = 'FORGED / IMPERSONATION ATTACK'
                reason = f'Empirical measurement error rate ({empirical_error_rate:.4f}) exceeds threshold ({acceptance_threshold:.2f}).'
                security_advice = 'Quantum state sequence mismatch. Signature forged or unauthorized sender.'

        return {
            'decision': decision,
            'threat_type': threat_type,
            'risk_indicator': risk_indicator,
            'authorization_status': 'AUTHORIZED',
            'replay_status': 'FRESH',
            'classical_integrity': classical_integrity,
            'error_rate': empirical_error_rate,
            'threshold': acceptance_threshold,
            'forgery_probability': forgery_prob,
            'verification_accuracy': stats['verification_accuracy'],
            'reason': reason,
            'security_advice': security_advice,
            'teleportation_results': teleportation_results,
            'stats': stats
        }

import time
import numpy as np


def run_threat_verification_pipeline(
    message: str,
    sender: str,
    verifier: str,
    scenario: str,
    num_measurements: int = 200,
    channel_noise: float = 0.05,
    acceptance_threshold: float = 0.05,
    seed: int = None
):
    if seed is not None:
        np.random.seed(seed)
        
    base_sig = generate_qds_signature(message, sender, verifier)
    
    scenario_str = scenario.upper().strip()
    
    if scenario_str.startswith('A') or 'LEGITIMATE' in scenario_str:
        sig_to_verify, v_id, noise, force_replay = simulate_attack_scenario('LEGITIMATE', base_sig, sender, verifier, channel_noise)
    elif scenario_str.startswith('B') or 'FORGED' in scenario_str:
        sig_to_verify, v_id, noise, force_replay = simulate_attack_scenario('FORGERY', base_sig, sender, verifier, channel_noise)
    elif scenario_str.startswith('C') or 'IMPERSONAT' in scenario_str:
        sig_to_verify, v_id, noise, force_replay = simulate_attack_scenario('IMPERSONATION', base_sig, sender, verifier, channel_noise)
    elif scenario_str.startswith('D') or 'REPLAY' in scenario_str:
        sig_to_verify, v_id, noise, force_replay = simulate_attack_scenario('REPLAY', base_sig, sender, verifier, channel_noise)
    elif scenario_str.startswith('E') or 'CHANNEL' in scenario_str:
        sig_to_verify, v_id, noise, force_replay = simulate_attack_scenario('CHANNEL_MANIPULATION', base_sig, sender, verifier, channel_noise)
    elif scenario_str.startswith('F') or 'UNAUTHORIZED' in scenario_str:
        sig_to_verify, v_id, noise, force_replay = simulate_attack_scenario('UNAUTHORIZED_VERIFIER', base_sig, sender, verifier, channel_noise)
    else:
        sig_to_verify, v_id, noise, force_replay = base_sig, verifier, channel_noise, False
        
    detector = QDSThreatDetector()
    res = detector.verify_signature(
        signature=sig_to_verify,
        verifier_id=v_id,
        num_shots=num_measurements,
        acceptance_threshold=acceptance_threshold,
        noise_level=noise,
        force_replay=force_replay
    )
    
    decision = res.get('decision', 'THREAT DETECTED')
    threat_type = res.get('threat_type', 'Threat Detected')
    error_rate = float(res.get('error_rate', 0.0))
    forgery_prob = float(res.get('forgery_probability', 0.0))
    auth_status = res.get('authorization_status', 'AUTHORIZED')
    replay_status = res.get('replay_status', 'FRESH')
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'decision': decision,
        'threat_type': threat_type,
        'sender_identity': sig_to_verify.get('sender_id', sender),
        'verifier_identity': v_id,
        'authorized_verifier': (auth_status == 'AUTHORIZED'),
        'message': message,
        'signature': sig_to_verify,
        'metrics': {
            'error_rate': error_rate,
            'threshold': acceptance_threshold,
            'forgery_probability': forgery_prob,
            'accuracy': res.get('verification_accuracy', 1.0 - error_rate),
            'matches': int((1.0 - error_rate) * num_measurements),
            'total_measurements': num_measurements
        },
        'replay_status': {
            'replay_detected': (replay_status == 'REPLAY_DETECTED')
        },
        'risk_level': res.get('risk_indicator', 'LOW'),
        'measurement_data': {
            'total_measurements': num_measurements,
            'matches': int((1.0 - error_rate) * num_measurements),
            'mismatches': int(error_rate * num_measurements),
            'expected_state': sig_to_verify.get('quantum_states', ['|0>'])[0],
            'counts': {
                sig_to_verify.get('quantum_states', ['|0>'])[0]: int((1.0 - error_rate) * num_measurements),
                'mismatch': int(error_rate * num_measurements)
            }
        }
    }
    return report

def clear_replay_ledger():
    SESSION_REPLAY_LEDGER.reset()

def get_session_ledger_size():
    return len(SESSION_REPLAY_LEDGER.seen_signatures) if hasattr(SESSION_REPLAY_LEDGER, 'seen_signatures') else 0
