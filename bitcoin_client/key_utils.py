from ecdsa import SECP256k1, SigningKey

def get_private_key(hex_string):
  # pad the hex string to the required 64 characters
  return bytes.fromhex(hex_string.zfill(64))

def get_public_key(private_key):
  return (bytes.fromhex("04") + SigningKey.from_string(private_key,
    curve=SECP256k1).verifying_key.to_string())

private_key = get_private_key("FEEDB0BDEADBEEF")
public_key = get_public_key(private_key)
