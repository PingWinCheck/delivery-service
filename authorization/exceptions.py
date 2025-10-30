from fastapi.exceptions import HTTPException

class ExpiredToken(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail='token expired')