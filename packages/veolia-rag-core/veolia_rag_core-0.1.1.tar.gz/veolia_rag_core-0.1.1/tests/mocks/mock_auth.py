"""
Mock implementation of authentication manager for testing.
"""

import logging
import secrets
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from security.user_manager import UserManager
from security.session_manager import SessionManager
from security.tenant_manager import TenantManager

logger = logging.getLogger(__name__)


class MockUserManager(UserManager):
    """
    Mock implementation of user manager.
    """

    def __init__(self):
        """
        Initialize mock user manager.
        """
        super().__init__()
        self._users: Dict[str, Dict[str, Any]] = {}

    async def create_user(
        self,
        user_id: str,
        tenant_id: str,
        email: str,
        name: str,
        permissions: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Mock user creation.

        Args:
            user_id (str): User identifier
            tenant_id (str): Tenant identifier
            email (str): User email
            name (str): User name
            permissions (List[str]): User permissions

        Returns:
            Dict[str, Any]: Created user
        """
        user = {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "email": email,
            "name": name,
            "permissions": permissions or [],
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
        }

        self._users[user_id] = user
        return user

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Mock user retrieval.

        Args:
            user_id (str): User identifier

        Returns:
            Optional[Dict[str, Any]]: User if found
        """
        return self._users.get(user_id)

    def get_users(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all users.

        Returns:
            Dict[str, Dict[str, Any]]: User ID to user mapping
        """
        return self._users.copy()


class MockSessionManager(SessionManager):
    """
    Mock implementation of session manager.
    """

    def __init__(self, user_manager: MockUserManager):
        """
        Initialize mock session manager.

        Args:
            user_manager (MockUserManager): User manager instance
        """
        super().__init__(user_manager)
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._tokens: Dict[str, str] = {}

    async def create_session(self, user_id: str, tenant_id: str) -> Dict[str, Any]:
        """
        Mock session creation.

        Args:
            user_id (str): User identifier
            tenant_id (str): Tenant identifier

        Returns:
            Dict[str, Any]: Created session
        """
        session_id = secrets.token_urlsafe(16)
        token = secrets.token_urlsafe(32)

        session = {
            "session_id": session_id,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "token": token,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            "is_active": True,
        }

        self._sessions[session_id] = session
        self._tokens[token] = session_id
        return session

    async def validate_session(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Mock session validation.

        Args:
            token (str): Session token

        Returns:
            Optional[Dict[str, Any]]: Session if valid
        """
        session_id = self._tokens.get(token)
        if not session_id:
            return None

        session = self._sessions.get(session_id)
        if not session or not session["is_active"]:
            return None

        return session

    def get_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all sessions.

        Returns:
            Dict[str, Dict[str, Any]]: Session ID to session mapping
        """
        return self._sessions.copy()


class MockTenantManager(TenantManager):
    """
    Mock implementation of tenant manager.
    """

    def __init__(self):
        """
        Initialize mock tenant manager.
        """
        super().__init__()
        self._tenants: Dict[str, Dict[str, Any]] = {}

    async def create_tenant(
        self, tenant_id: str, name: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Mock tenant creation.

        Args:
            tenant_id (str): Tenant identifier
            name (str): Tenant name
            description (Optional[str]): Tenant description

        Returns:
            Dict[str, Any]: Created tenant
        """
        tenant = {
            "tenant_id": tenant_id,
            "name": name,
            "description": description,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "config": {
                "max_users": 10,
                "max_storage": 1024,
                "allowed_extensions": ["pdf", "txt", "csv", "docx"],
                "max_file_size": 10,
            },
        }

        self._tenants[tenant_id] = tenant
        return tenant

    async def get_tenant(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """
        Mock tenant retrieval.

        Args:
            tenant_id (str): Tenant identifier

        Returns:
            Optional[Dict[str, Any]]: Tenant if found
        """
        return self._tenants.get(tenant_id)

    def get_tenants(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all tenants.

        Returns:
            Dict[str, Dict[str, Any]]: Tenant ID to tenant mapping
        """
        return self._tenants.copy()
