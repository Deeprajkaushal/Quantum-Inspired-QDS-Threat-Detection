import pytest
from security.authorization import (
    AUTHORIZED_VERIFIERS,
    is_authorized_verifier,
    get_authorized_verifiers,
    VerifierAuthorization
)

def test_authorized_verifiers_list():
    assert "VERIFIER_A" in AUTHORIZED_VERIFIERS
    assert "VERIFIER_B" in AUTHORIZED_VERIFIERS
    assert "VERIFIER_C" in AUTHORIZED_VERIFIERS

def test_is_authorized_verifier_func():
    assert is_authorized_verifier("VERIFIER_A") is True
    assert is_authorized_verifier("UNAUTHORIZED_EVE") is False

def test_get_authorized_verifiers_func():
    verifiers = get_authorized_verifiers()
    assert isinstance(verifiers, list)
    assert verifiers == AUTHORIZED_VERIFIERS

def test_verifier_authorization_class():
    auth = VerifierAuthorization()
    assert auth.is_authorized("VERIFIER_A") is True
    assert auth.is_authorized("UNAUTHORIZED_EVE") is False

    custom_auth = VerifierAuthorization(["CUSTOM_VERIFIER"])
    assert custom_auth.is_authorized("CUSTOM_VERIFIER") is True
    assert custom_auth.is_authorized("VERIFIER_A") is False
