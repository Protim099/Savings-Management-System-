import hashlib
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def authenticate(email, password):
    try:
        user = User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None
    return user if user.is_active and user.password_hash == hash_password(password) else None

def tokens_for_user(user):
    refresh = RefreshToken()
    refresh["user_id"] = str(user.id)
    refresh["role"] = user.role
    refresh["email"] = user.email
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
