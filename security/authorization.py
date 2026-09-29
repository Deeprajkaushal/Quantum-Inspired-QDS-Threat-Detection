class VerifierAuthorization:
    def __init__(self, authorized_list: list = None):
        if authorized_list is None:
            self.authorized_verifiers = ['VERIFIER_A', 'VERIFIER_B', 'VERIFIER_C']
        else:
            self.authorized_verifiers = authorized_list

    def is_authorized(self, verifier_id: str) -> bool:
        return verifier_id in self.authorized_verifiers
