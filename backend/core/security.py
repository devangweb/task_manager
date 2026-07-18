# core/security.py
import os
import jwt
from datetime import datetime, timedelta
# from passlib.context import CryptContext
from pwdlib import PasswordHash



SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated="auto")
# Initialize secure modern password hashing
password_engine = PasswordHash.recommended()

#  def _normalize_password(password: str) -> str:
#     """Normalize and truncate password to bcrypt's 72-byte limit.

#     bcrypt only considers the first 72 bytes of the password. To avoid
#     runtime errors when a user provides a longer password, truncate the
#     UTF-8 encoded bytes to 72 and decode back to a string, ignoring any
#     partial multibyte sequence at the end.
#     """
    
#     if password is None:
#         return password
#     b = password.encode("utf-8")
#     if len(b) <= 72:
#         return password
#     truncated = b[:72]
#     return truncated.decode("utf-8", "ignore")


def verify_password(plain_password: str, hashed_password: str) -> bool:
     return password_engine.verify(plain_password, hashed_password)
    # return pwd_context.verify(_normalize_password(plain_password), hashed_password)


def get_password_hash(password: str) -> str:
    print(f"Normalizing password for hashing: {password}")
    return password_engine.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt