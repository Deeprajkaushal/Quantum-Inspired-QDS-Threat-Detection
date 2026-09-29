import numpy as np

def calculate_verification_stats(
    expected_states: list,
    teleported_results: list,
    num_shots_per_state: int = 500
) -> dict:
    total_shots = 0
    total_matches = 0
    total_mismatches = 0
    token_details = []

    for expected_name, result in zip(expected_states, teleported_results):
        fid = result['fidelity']
        expected_prob = fid

        mismatches = int(np.round(num_shots_per_state * (1.0 - expected_prob)))
        matches = num_shots_per_state - mismatches

        total_shots += num_shots_per_state
        total_matches += matches
        total_mismatches += mismatches

        token_details.append({
            'expected_state': expected_name,
            'teleported_state_name': result['teleported_state_name'],
            'fidelity': fid,
            'matches': matches,
            'mismatches': mismatches,
            'error_rate': mismatches / num_shots_per_state
        })

    empirical_error_rate = total_mismatches / total_shots if total_shots > 0 else 0.0
    verification_accuracy = total_matches / total_shots if total_shots > 0 else 0.0

    return {
        'total_tokens': len(expected_states),
        'total_shots': total_shots,
        'total_matches': total_matches,
        'total_mismatches': total_mismatches,
        'empirical_error_rate': empirical_error_rate,
        'verification_accuracy': verification_accuracy,
        'token_details': token_details
    }

def compute_forgery_probability(error_rate: float, num_measurements: int = 200) -> float:
    if error_rate <= 0.05:
        return float(np.clip(error_rate * 2.0, 0.0, 0.10))
    else:
        return float(np.clip(1.0 - np.exp(-5.0 * (error_rate - 0.05)), 0.10, 0.999))