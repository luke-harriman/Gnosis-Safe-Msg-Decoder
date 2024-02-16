from web3 import Web3
import ecdsa
import hashlib
import sha3
from typing import List, Tuple
from coincurve import PublicKey
from eth_account import Account
from eth_account.messages import defunct_hash_message
from eth_keys import keys
from eth_utils import to_checksum_address
from eth_keys import KeyAPI
from eth_keys.datatypes import Signature
from eth_utils import keccak
import textwrap
from typing import List, Tuple
from eth_account.messages import SignableMessage

def ecrecover(msg_hash: bytes, v: int, r: bytes, s: bytes) -> bytes:
    def set_length(buffer: bytes, length: int) -> bytes:
        return buffer.ljust(length, b'\x00')

    signature = set_length(r, 32) + set_length(s, 32)
    recovery = v - 27
    if recovery not in (0, 1):
        raise ValueError('Invalid signature v value')

    public_key = PublicKey.from_signature_and_message(
        signature + bytes([recovery]), msg_hash, hasher=None)

    recovery = v - 27
    if recovery not in (0, 1):
        print("Invalid signature v value")
        return None

    return public_key.format(compressed=False)[1:]


def parse_rsv(blob: str) -> Tuple[int, bytes, bytes]:
    r = bytes.fromhex(blob[2:66])
    s = bytes.fromhex(blob[66:130])
    v = int(blob[130:132], 16)
    return r, s, v

def public_key_to_address(public_key: bytes) -> str:
    public_key_obj = keys.PublicKey(public_key)
    return to_checksum_address(public_key_obj.to_address()[2:])

def recover_signer_addresses(encoded_signatures: str, msg_hash: bytes) -> List[Tuple[str, str]]:
    # If the encoded signatures string is 40 characters long, return it as is.
    if len(encoded_signatures) == 42:
        return [(encoded_signatures, "")]
    signatures = bytes.fromhex(encoded_signatures[2:])
    signer_data = []
    i = 0
    while i < len(signatures):
        r = signatures[i:i + 32]
        s = signatures[i + 32:i + 64]
        signature_type = int.from_bytes(signatures[i + 64:i + 65], byteorder='big')
        step_size = 65  # Default step size for ECDSA and eth_sign signatures
        
        if 26 <= signature_type <= 31:  # ECDSA Signature
            v = signature_type
            public_key = ecrecover(msg_hash, v, r, s)
            if public_key is not None:
                public_key_bytes = bytes.fromhex(public_key.hex())
                address = public_key_to_address(public_key_bytes)
                signer_data.append((address, "ECDSA Signature"))
        elif signature_type == 28 or signature_type == 27:  # eth_sign signature
            v = signature_type - 2
            public_key = ecrecover(msg_hash, v, r, s)
            if public_key is not None:
                public_key_bytes = bytes.fromhex(public_key.hex())
                address = public_key_to_address(public_key_bytes)
                signer_data.append((address, "eth_sign Signature"))
        elif signature_type == 0:  # Contract Signature (EIP-1271)
            # Implement the logic for EIP-1271 Contract Signature handling
            pass
        elif signature_type == 1:  # Pre-Validated Signature
            signer_data.append((to_checksum_address('0x' + signatures[i+12:i + 32].hex()), "Pre-Validated Signature"))
            step_size = 65  # Pre-Validated Signature is 52 bytes long
        else:
            print(f"Unrecognized signature type: {signature_type}, skipping...")
        
        i += step_size  # Move to the next signature
    return signer_data

# Log event data
encoded_signatures = ""
msg_hash = bytes.fromhex("")

signer_data = recover_signer_addresses(encoded_signatures, msg_hash)

print("Signer Data:")
for address, signature_type in signer_data:
    print(f"Address: {address}, Signature Type: {signature_type}")