from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from passlib.context import CryptContext
from .config import settings

SESSION_COOKIE  = "fitbuddy_session"
SESSION_MAX_AGE = 3600

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_serializer  = None


def _get_serializer():
    global _serializer
    if _serializer is None:
        _serializer = URLSafeTimedSerializer(settings.secret_key)
    return _serializer


def hash_password(plain: str) -> str:
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


def check_admin(username: str, password: str) -> bool:
    return (
        username == settings.admin_username
        and password == settings.admin_password
    )


def create_session_token(username: str) -> str:
    return _get_serializer().dumps(username, salt="admin-session")


def verify_session_token(token: str) -> bool:
    try:
        _get_serializer().loads(token, salt="admin-session", max_age=SESSION_MAX_AGE)
        return True
    except (BadSignature, SignatureExpired):
        return False
