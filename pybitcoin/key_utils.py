import binascii
import hashlib
import os

from ecdsa import SECP256k1, SigningKey

def get_private_key(hex_string):
  # pad the hex string to the required 64 characters
  return bytes.fromhex(hex_string.zfill(64))


def get_random_private_key():
  return os.urandom(32)


# From https://en.wikipedia.org/wiki/Base58#cite_note-2 (see 'Bitcoin
# addresses')
_alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def get_base58_encode(bytes_num):
  num = int.from_bytes(bytes_num, byteorder='big')
  base_count = len(_alphabet)
  encode = ''
  while (num > 0):
    num, mod = divmod(num, base_count)
    encode = _alphabet[mod] + encode
  return encode


def get_wallet_import_format(private_key):
  assert isinstance(private_key, bytes)
  arr = bytearray(private_key)
  # 1) Add a 0x80 byte in front of it for mainnet
  arr.insert(0, 0x80)
  # 2) Perform SHA-256 hash on the extended key
  res1 = hashlib.sha256(bytes(arr)).digest()
  # 2) Perform SHA-256 hash on the extended key
  res2 = hashlib.sha256(res1).digest()
  # Take the first 4 bytes of the second SHA-256 hash, this is the checksum
  checksum = res2[:4]
  arr.extend(checksum)
  return get_base58_encode(arr)


def get_public_key(private_key):
  return (bytes.fromhex("04") + SigningKey.from_string(private_key,
      curve=SECP256k1).verifying_key.to_string())


def get_public_address(public_key):
  address = hashlib.sha256(public_key).digest()

  h = hashlib.new('ripemd160')
  h.update(address)
  address = h.digest()

  return address

# 58 character alphabet used
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(version, public_address):
  """
  Gets a Base58Check string
  See https://en.bitcoin.it/wiki/base58Check_encoding
  """
  version = bytes.fromhex(version)
  checksum = hashlib.sha256(hashlib.sha256(version + public_address).digest()).digest()[:4]
  payload = version + public_address + checksum

  result = int.from_bytes(payload, byteorder="big")

  # count the leading 0s
  padding = len(payload) - len(payload.lstrip(b'\0'))
  encoded = []

  while result != 0:
      result, remainder = divmod(result, 58)
      encoded.append(BASE58_ALPHABET[remainder])

  return padding*"1" + "".join(encoded)[::-1]

def get_btc_address(private_key):
  public_key = get_public_key(private_key)
  public_address = get_public_address(public_key)
  bitcoin_address = base58_encode("00", public_address)
  return bitcoin_address
