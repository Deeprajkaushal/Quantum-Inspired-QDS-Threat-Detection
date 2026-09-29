import numpy as np
from quantum.states import normalize, fidelity, state_to_name
from quantum.gates import apply_gate, get_pauli_correction, X_GATE, Z_GATE, Y_GATE
from quantum.bell import create_bell_pair

def teleport_qubit(
    input_state: np.ndarray,
    noise_prob: float = 0.0,
    noise_type: str = 'depolarizing',
    seed: int = None
) -> dict:
    input_state = normalize(input_state)
    rng = np.random.RandomState(seed)

    bell_ab = create_bell_pair('PHI_PLUS')

    bsm_outcomes = [(0, 0), (1, 0), (0, 1), (1, 1)]
    m1, m2 = bsm_outcomes[rng.choice(4)]

    raw_states = {
        (0, 0): input_state.copy(),
        (1, 0): apply_gate(Z_GATE, input_state),
        (0, 1): apply_gate(X_GATE, input_state),
        (1, 1): apply_gate(np.dot(X_GATE, Z_GATE), input_state)
    }
    bob_state = raw_states[(m1, m2)]

    noise_applied = 'none'
    if noise_prob > 0 and rng.rand() < noise_prob:
        if noise_type == 'bit_flip':
            bob_state = apply_gate(X_GATE, bob_state)
            noise_applied = 'Pauli X (Bit Flip)'
        elif noise_type == 'phase_flip':
            bob_state = apply_gate(Z_GATE, bob_state)
            noise_applied = 'Pauli Z (Phase Flip)'
        else:
            op_name = rng.choice(['X', 'Y', 'Z'])
            if op_name == 'X':
                bob_state = apply_gate(X_GATE, bob_state)
            elif op_name == 'Y':
                bob_state = apply_gate(Y_GATE, bob_state)
            else:
                bob_state = apply_gate(Z_GATE, bob_state)
            noise_applied = f'Pauli {op_name}'

    correction_matrix = get_pauli_correction(m1, m2)
    teleported_state = apply_gate(correction_matrix, bob_state)
    fid = fidelity(input_state, teleported_state)

    return {
        'input_state': input_state,
        'input_state_name': state_to_name(input_state),
        'classical_bits': (m1, m2),
        'correction_pauli': f'Z^{m1} X^{m2}',
        'noise_applied': noise_applied,
        'teleported_state': teleported_state,
        'teleported_state_name': state_to_name(teleported_state),
        'fidelity': fid
    }
