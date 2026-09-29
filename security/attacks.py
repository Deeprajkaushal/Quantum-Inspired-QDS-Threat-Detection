import copy

def simulate_attack_scenario(
    scenario_key: str,
    original_sig: dict,
    attacker_sender: str = 'ATTACKER_EVE',
    verifier: str = 'VERIFIER_A',
    noise_level: float = 0.25
) -> tuple:
    sig = copy.deepcopy(original_sig)
    force_replay = False
    applied_noise = 0.0

    if scenario_key == 'LEGITIMATE':
        return sig, verifier, 0.0, False

    elif scenario_key == 'FORGERY':
        sig['message'] = sig['message'] + ' (TAMPERED)'
        for i in range(len(sig['quantum_states'])):
            if i % 2 == 0:
                sig['quantum_states'][i] = '|1>' if sig['quantum_states'][i] == '|0>' else '|0>'
        return sig, verifier, 0.0, False

    elif scenario_key == 'IMPERSONATION':
        sig['sender_id'] = attacker_sender
        sig['message_digest'] = 'TAMPERED_IMPERSONATED_DIGEST_' + sig.get('message_digest', '')
        return sig, verifier, 0.0, False

    elif scenario_key == 'REPLAY':
        force_replay = True
        return sig, verifier, 0.0, force_replay

    elif scenario_key == 'CHANNEL_MANIPULATION':
        applied_noise = max(0.15, noise_level)
        return sig, verifier, applied_noise, False

    elif scenario_key == 'UNAUTHORIZED_VERIFIER':
        unauthorized_verifier = 'VERIFIER_UNAUTHORIZED_MALLORY'
        return sig, unauthorized_verifier, 0.0, False

    return sig, verifier, 0.0, False
