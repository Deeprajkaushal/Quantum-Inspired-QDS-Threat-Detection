import pytest
import numpy as np
from quantum.states import (
    ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I,
    normalize, fidelity
)
from quantum.gates import I_GATE, X_GATE, Y_GATE, Z_GATE, H_GATE, S_GATE, tensor_product

def test_pauli_eigenstates_normalization():
    states = [("|0>", ZERO), ("|1>", ONE), ("|+>", PLUS), ("|->", MINUS), ("|+i>", PLUS_I), ("|-i>", MINUS_I)]
    for name, state in states:
        norm = np.linalg.norm(state)
        assert np.isclose(norm, 1.0), f"State {name} is not normalized"

def test_state_fidelity():
    assert np.isclose(fidelity(ZERO, ZERO), 1.0)
    assert np.isclose(fidelity(ZERO, ONE), 0.0)
    assert np.isclose(fidelity(PLUS, MINUS), 0.0)
    assert np.isclose(fidelity(ZERO, PLUS), 0.5)

def test_pauli_operators():
    assert np.allclose(X_GATE @ ZERO, ONE)
    assert np.allclose(X_GATE @ ONE, ZERO)
    assert np.allclose(Z_GATE @ ZERO, ZERO)
    assert np.allclose(Z_GATE @ ONE, -ONE)
    assert np.allclose(H_GATE @ ZERO, PLUS)
    assert np.allclose(H_GATE @ ONE, MINUS)

def test_tensor_product():
    k00 = tensor_product(ZERO, ZERO)
    assert k00.shape == (4,)
    assert np.allclose(k00, np.array([1, 0, 0, 0]))
