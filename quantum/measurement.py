import numpy as np
from quantum.states import ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I, normalize

BASIS_MAP = {
    'Z': [('|0>', ZERO), ('|1>', ONE)],
    'X': [('|+>', PLUS), ('|->', MINUS)],
    'Y': [('|+i>', PLUS_I), ('|-i>', MINUS_I)]
}

def measure_basis(
    state: np.ndarray,
    basis: str = 'Z',
    num_shots: int = 500,
    seed: int = None
) -> dict:
    state = normalize(state)
    basis = basis.upper()
    if basis not in BASIS_MAP:
        raise ValueError(f'Unsupported measurement basis {basis}.')

    eigenstates = BASIS_MAP[basis]
    labels = [e[0] for e in eigenstates]

    probs = [float(np.abs(np.vdot(e[1], state))**2) for e in eigenstates]
    total_p = sum(probs)
    if total_p > 0:
        probs = [p / total_p for p in probs]

    rng = np.random.RandomState(seed)
    samples = rng.choice(len(labels), size=num_shots, p=probs)
    counts = {labels[i]: int(np.sum(samples == i)) for i in range(len(labels))}

    return {
        'basis': basis,
        'num_shots': num_shots,
        'probabilities': dict(zip(labels, probs)),
        'counts': counts,
        'dominant_outcome': labels[np.argmax(probs)]
    }
