from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "Lock"


def create_token(data: dict, secret_key: str = SECRET_KEY):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str, secret_key: str = SECRET_KEY):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except Exception:
        return None
