import numpy as np

I_GATE = np.eye(2, dtype=complex)
X_GATE = np.array([[0, 1], [1, 0]], dtype=complex)
Y_GATE = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z_GATE = np.array([[1, 0], [0, -1]], dtype=complex)

H_GATE = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S_GATE = np.array([[1, 0], [0, 1j]], dtype=complex)

CNOT_GATE = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

def tensor_product(*matrices) -> np.ndarray:
    result = matrices[0]
    for m in matrices[1:]:
        result = np.kron(result, m)
    return result

def apply_gate(gate: np.ndarray, state: np.ndarray) -> np.ndarray:
    result = np.dot(gate, state)
    norm = np.linalg.norm(result)
    if norm > 0:
        result = result / norm
    return result

def get_pauli_correction(m1: int, m2: int) -> np.ndarray:
    op = np.eye(2, dtype=complex)
    if m2 == 1:
        op = np.dot(X_GATE, op)
    if m1 == 1:
        op = np.dot(Z_GATE, op)
    return op
