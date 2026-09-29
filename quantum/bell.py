import numpy as np
from quantum.states import ZERO, ONE, normalize
from quantum.gates import tensor_product

PHI_PLUS = (tensor_product(ZERO, ZERO) + tensor_product(ONE, ONE)) / np.sqrt(2)
PHI_MINUS = (tensor_product(ZERO, ZERO) - tensor_product(ONE, ONE)) / np.sqrt(2)
PSI_PLUS = (tensor_product(ZERO, ONE) + tensor_product(ONE, ZERO)) / np.sqrt(2)
PSI_MINUS = (tensor_product(ZERO, ONE) - tensor_product(ONE, ZERO)) / np.sqrt(2)

BELL_STATES = {
    'PHI_PLUS': PHI_PLUS,
    'PHI_MINUS': PHI_MINUS,
    'PSI_PLUS': PSI_PLUS,
    'PSI_MINUS': PSI_MINUS
}

def create_bell_pair(bell_type: str = 'PHI_PLUS') -> np.ndarray:
    if bell_type not in BELL_STATES:
        raise ValueError(f'Invalid Bell state {bell_type}')
    return BELL_STATES[bell_type].copy()

def bell_measurement(two_qubit_state: np.ndarray, seed: int = None) -> tuple:
    two_qubit_state = normalize(two_qubit_state)
    probs = [
        float(np.abs(np.vdot(PHI_PLUS, two_qubit_state))**2),
        float(np.abs(np.vdot(PHI_MINUS, two_qubit_state))**2),
        float(np.abs(np.vdot(PSI_PLUS, two_qubit_state))**2),
        float(np.abs(np.vdot(PSI_MINUS, two_qubit_state))**2)
    ]
    total = sum(probs)
    if total > 0:
        probs = [p / total for p in probs]

    rng = np.random.RandomState(seed)
    idx = rng.choice(4, p=probs)
    outcomes = [
        (0, 0, 'PHI_PLUS'),
        (1, 0, 'PHI_MINUS'),
        (0, 1, 'PSI_PLUS'),
        (1, 1, 'PSI_MINUS')
    ]
    return outcomes[idx]
