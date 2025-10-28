from typing import Sequence

import jwt


class JWT:
    def __init__(self, key: str, algorithms: Sequence[str]):
        self.key = key
        self.algorithms = algorithms

    def decode(self, token: str) -> dict:
        decode_ = jwt.decode(jwt=token, key=self.key, algorithms=self.algorithms)
        return decode_