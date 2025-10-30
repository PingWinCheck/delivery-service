from typing import Sequence
from jwt.exceptions import ExpiredSignatureError
from .exceptions import ExpiredToken

import jwt


class JWT:
    def __init__(self, key: str, algorithms: Sequence[str]):
        self.key = key
        self.algorithms = algorithms

    def decode(self, token: str) -> dict:
        try:
            decode_ = jwt.decode(jwt=token, key=self.key, algorithms=self.algorithms)
        except ExpiredSignatureError:
            raise ExpiredToken
        return decode_