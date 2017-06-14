from ecdsa import SECP256k1, SigningKey

def get_private_key(hex_string):
  # pad the hex string to the required 64 characters
  return bytearray.fromhex(hex_string.zfill(64))

def get_public_key(private_key):
  return "04" + (bytearray.fromhex(SigningKey.from_string(private_key,
      curve=SECP256k1).verifying_key.to_string()))
