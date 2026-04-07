from jose import JWTError, jwt

SECRET_KEY = "Lock"  # In a real app, this should be a secure secret key

ALGORITHM = "HS256"

def create_access_token(data: dict, secret_key: str):
    return jwt.encode(data, secret_key, algorithm=ALGORITHM)

def decode_access_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None