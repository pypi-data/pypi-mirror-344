from typing import List, Dict, Tuple
from enum import Enum

class Intermediates:
    intermediates: Dict[bytes, List[bytes]]
    def add_cert(self, issuer_dn: bytes, der_cert: bytes) -> None: ...
    def to_bincode(self) -> List[bytes]: ...
    def from_bincode(self, bytes) -> Intermediates: ...

class PyCRLiteStatus(Enum):
    Good = 0
    NotCovered = 1
    NotEnrolled =2
    Revoked = 3

class PyCRLiteClubcard:
    def load_filter(filter_bytes: bytes) -> PyCRLiteClubcard: ...
    def query_filter(filter: PyCRLiteClubcard, issuer_spki_hash: bytes, serial: bytes, timestamps: List[Tuple[bytes, int]]) -> PyCRLiteStatus: ...