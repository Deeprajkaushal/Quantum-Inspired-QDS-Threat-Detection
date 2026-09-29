AUTHORIZED_VERIFIERS = ['VERIFIER_A', 'VERIFIER_B', 'VERIFIER_C']


def is_authorized_verifier(verifier_id: str) -> bool:
    """Check if a verifier_id is in the authorized verifiers list."""
    return verifier_id in AUTHORIZED_VERIFIERS


def get_authorized_verifiers() -> list:
    """Return a list of authorized verifiers."""
    return list(AUTHORIZED_VERIFIERS)


class VerifierAuthorization:
    """Authorization controller for QDS verifiers."""

    def __init__(self, authorized_list: list = None):
        if authorized_list is None:
            self.authorized_verifiers = list(AUTHORIZED_VERIFIERS)
        else:
            self.authorized_verifiers = list(authorized_list)

    def is_authorized(self, verifier_id: str) -> bool:
        return verifier_id in self.authorized_verifiers

