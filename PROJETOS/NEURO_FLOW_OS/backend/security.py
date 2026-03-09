import jwt
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

SECRET_KEY = "antigravity_sovereign_secret"

class BioSecurity:
    """
    Simulates Bio-JWT and E2EE for BrainState logs.
    """
    
    @staticmethod
    def generate_bio_jwt(user_id: str, bio_digest: str) -> str:
        payload = {
            "sub": user_id,
            "bio_hash": bio_digest,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
            "iss": "NEURO-FLOW-OS-KERNEL"
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def encrypt_brain_data(data: str, bio_hash: str) -> bytes:
        # Derive key from bio_hash
        salt = b'sovereign_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(bio_hash.encode())
        
        # AES-GCM Encryption
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        
        ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext

# Example Usage simulation
# token = BioSecurity.generate_bio_jwt("user_01", "iris_digest_xyz")
