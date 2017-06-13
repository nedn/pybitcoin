import os
import sys


def _AddToPathIfNeeded(path):
  if path not in sys.path:
    sys.path.insert(0, path)

_TOP_LEVEL_DIR = os.path.join(os.path.dirname(__file__), '..')
_THIRD_PARTY_DIR = os.path.join(_TOP_LEVEL_DIR, 'third_party')

_AddToPathIfNeeded(os.path.join(_THIRD_PARTY_DIR, 'python-ecdsa', 'src'))
_AddToPathIfNeeded(os.path.join(_THIRD_PARTY_DIR, 'six'))
