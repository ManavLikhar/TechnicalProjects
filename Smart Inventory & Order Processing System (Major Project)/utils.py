from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "Lock"  # In a real app, this should be a secure secret key

ALGORITHM = "HS256" # Algorithm used to sign and verify tokens

# Create access token
def create_access_token(data: dict, secret_key: str): 
    to_encode = data.copy() # Create a copy of the data
    expire = datetime.utcnow() + timedelta(minutes=30) # Set the expiration time
    to_encode.update({"exp": expire}) # Add the expiration time to the payload
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM) # Encode the payload

# Decode access token
def decode_access_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM]) # Decode the token
        return payload # Return the payload
    except JWTError:
        return None