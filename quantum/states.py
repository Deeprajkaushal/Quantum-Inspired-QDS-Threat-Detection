import numpy as np

ZERO = np.array([1.0, 0.0], dtype=complex)
ONE = np.array([0.0, 1.0], dtype=complex)

PLUS = (ZERO + ONE) / np.sqrt(2)
MINUS = (ZERO - ONE) / np.sqrt(2)

PLUS_I = (ZERO + 1j * ONE) / np.sqrt(2)
MINUS_I = (ZERO - 1j * ONE) / np.sqrt(2)

EIGENSTATES = {
    '|0>': ZERO,
    '|1>': ONE,
    '|+>': PLUS,
    '|->': MINUS,
    '|+i>': PLUS_I,
    '|-i>': MINUS_I
}

def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError('State vector norm cannot be zero.')
    return state / norm

def fidelity(state_a: np.ndarray, state_b: np.ndarray) -> float:
    inner_product = np.vdot(state_a, state_b)
    return float(np.abs(inner_product)**2)

def name_to_state(name: str) -> np.ndarray:
    if name not in EIGENSTATES:
        raise KeyError(f'Unknown state {name}')
    return EIGENSTATES[name].copy()

def state_to_name(state: np.ndarray, atol: float = 1e-4) -> str:
    for name, ref_state in EIGENSTATES.items():
        if fidelity(state, ref_state) >= (1.0 - atol):
            return name
    return 'Custom State'
