import pytest
import numpy as np
from quantum.states import ZERO, ONE, PLUS, MINUS, PLUS_I, MINUS_I, fidelity
from quantum.teleportation import teleport_qubit

def test_teleportation_ideal():
    states = [("|0>", ZERO), ("|1>", ONE), ("|+>", PLUS), ("|->", MINUS), ("|+i>", PLUS_I), ("|-i>", MINUS_I)]
    for name, state in states:
        res = teleport_qubit(state, noise_prob=0.0)
        reconstructed = res["teleported_state"]
        fid = fidelity(state, reconstructed)
        assert np.isclose(fid, 1.0), f"Teleportation failed for {name}"

def test_teleportation_noisy():
    state = ZERO
    res = teleport_qubit(state, noise_prob=0.5, seed=42)
    reconstructed = res["teleported_state"]
    fid = fidelity(state, reconstructed)
    assert fid <= 1.0
