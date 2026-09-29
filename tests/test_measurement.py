import pytest
from quantum.states import ZERO, ONE, PLUS, PLUS_I
from quantum.measurement import measure_basis
from quantum.statistics import compute_forgery_probability

def test_measurement_outcomes():
    res = measure_basis(ZERO, basis="Z", num_shots=100, seed=42)
    counts = res.get("counts", {})
    assert counts.get("|0>", 0) == 100

def test_forgery_probability():
    prob_low = compute_forgery_probability(error_rate=0.01, num_measurements=200)
    prob_high = compute_forgery_probability(error_rate=0.50, num_measurements=200)
    assert prob_low < prob_high
