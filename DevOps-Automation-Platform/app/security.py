"""Security module for JWT authentication and RBAC"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

from app.config import settings
from app.utils.logger import logger

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


class SecurityManager:
    """Manages JWT tokens and authentication"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                hours=settings.JWT_EXPIRATION_HOURS
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.error(f"JWT decode error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )


class RBACManager:
    """Manages Role-Based Access Control"""

    ROLES = {
        "admin": ["read", "write", "approve", "delete"],
        "approver": ["read", "approve"],
        "deployer": ["read", "write"],
        "viewer": ["read"],
    }

    @staticmethod
    def has_permission(user_role: str, required_permission: str) -> bool:
        """Check if user role has required permission"""
        permissions = RBACManager.ROLES.get(user_role, [])
        return required_permission in permissions

    @staticmethod
    def require_role(*allowed_roles: str):
        """Dependency to require specific roles"""
        async def role_checker(current_user: Dict = Depends(get_current_user)):
            if current_user.get("role") not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return current_user

        return role_checker


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> Dict:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials

    try:
        payload = SecurityManager.decode_token(token)
        user_id: str = payload.get("sub")
        role: str = payload.get("role", "viewer")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "role": role,
            "permissions": RBACManager.ROLES.get(role, [])
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_admin_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """Dependency to require admin role"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def get_approver_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """Dependency to require approver role"""
    if current_user.get("role") not in ["admin", "approver"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Approver access required"
        )
    return current_user
