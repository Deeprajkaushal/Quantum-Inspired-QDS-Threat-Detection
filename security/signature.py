import hashlib
import uuid
import datetime
import numpy as np

def generate_qds_signature(
    message: str,
    sender_id: str,
    verifier_id: str,
    secret_key: str = 'SECRET_KEY_123'
) -> dict:
    message_digest = hashlib.sha256(message.encode('utf-8')).hexdigest()
    signature_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    nonce = str(int(hashlib.md5(f'{signature_id}{timestamp}'.encode()).hexdigest(), 16) % 10000000)

    seed_val = int(hashlib.sha256(f'{message_digest}{secret_key}'.encode()).hexdigest()[:8], 16)
    rng = np.random.RandomState(seed_val)

    basis_pool = ['Z', 'X', 'Y']
    state_pool = {
        'Z': ['|0>', '|1>'],
        'X': ['|+>', '|->'],
        'Y': ['|+i>', '|-i>']
    }

    basis_sequence = []
    quantum_states = []

    for _ in range(8):
        b = rng.choice(basis_pool)
        s = rng.choice(state_pool[b])
        basis_sequence.append(b)
        quantum_states.append(s)

    return {
        'message': message,
        'message_digest': message_digest,
        'sender_id': sender_id,
        'verifier_id': verifier_id,
        'signature_id': signature_id,
        'timestamp': timestamp,
        'nonce': nonce,
        'basis_sequence': basis_sequence,
        'bases': basis_sequence,
        'quantum_states': quantum_states,
        'classical_metadata_label': 'Classical metadata / integrity layer',
        'quantum_signature_label': 'Simulated quantum-signature verification layer'
    }

def verify_classical_integrity(message: str, signature: dict) -> bool:
    computed = hashlib.sha256(message.encode('utf-8')).hexdigest()
    return computed == signature.get('message_digest', '')