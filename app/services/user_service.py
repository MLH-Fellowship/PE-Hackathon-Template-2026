"""
User Service Layer

This module contains the business logic for user operations.
It acts as an intermediary between the routes and the repository layers.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime


class UserService:
    """Service class for user-related business logic"""
    
    def __init__(self, user_repository):
        """
        Initialize the UserService
        
        Args:
            user_repository: Repository instance for database operations
        """
        self.user_repository = user_repository
    
    def get_all_users(
        self, 
        page: int = 1, 
        limit: int = 20, 
        sort: str = 'created_at',
        order: str = 'asc'
    ) -> Dict[str, Any]:
        """
        Get all users with pagination
        
        Args:
            page: Page number
            limit: Items per page
            sort: Field to sort by
            order: Sort order (asc/desc)
            
        Returns:
            Dict containing users data and pagination info
        """
        # Validate pagination parameters
        page = max(1, page)
        limit = min(max(1, limit), 100)  # Max 100 items per page
        
        # Get users from repository
        offset = (page - 1) * limit
        users = self.user_repository.find_all(
            offset=offset,
            limit=limit,
            sort=sort,
            order=order
        )
        total = self.user_repository.count()
        
        # Calculate pagination metadata
        total_pages = (total + limit - 1) // limit
        
        return {
            "data": [self._serialize_user(user) for user in users],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": total_pages
            }
        }
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a single user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User data or None if not found
        """
        user = self.user_repository.find_by_id(user_id)
        if user:
            return {"data": self._serialize_user(user)}
        return None
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user
        
        Args:
            user_data: User data containing username, email, password
            
        Returns:
            Created user data
            
        Raises:
            ValueError: If validation fails
            ConflictError: If username or email already exists
        """
        # Validate required fields
        self._validate_user_data(user_data)
        
        # Check for existing username or email
        if self.user_repository.find_by_username(user_data['username']):
            raise ConflictError("Username already exists")
        if self.user_repository.find_by_email(user_data['email']):
            raise ConflictError("Email already exists")
        
        # Hash password before storing
        user_data['password'] = self._hash_password(user_data['password'])
        
        # Create user
        user = self.user_repository.create(user_data)
        return {"data": self._serialize_user(user)}
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an entire user
        
        Args:
            user_id: User ID
            user_data: Complete user data
            
        Returns:
            Updated user data or None if not found
            
        Raises:
            ValueError: If validation fails
            ConflictError: If username or email already exists
        """
        # Check if user exists
        existing_user = self.user_repository.find_by_id(user_id)
        if not existing_user:
            return None
        
        # Validate data
        self._validate_user_data(user_data)
        
        # Check for conflicts (excluding current user)
        self._check_conflicts(user_data, user_id)
        
        # Hash password if provided
        if 'password' in user_data:
            user_data['password'] = self._hash_password(user_data['password'])
        
        # Update user
        updated_user = self.user_repository.update(user_id, user_data)
        return {"data": self._serialize_user(updated_user)}
    
    def partial_update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Partially update a user
        
        Args:
            user_id: User ID
            user_data: Partial user data
            
        Returns:
            Updated user data or None if not found
            
        Raises:
            ConflictError: If email already exists
        """
        # Check if user exists
        existing_user = self.user_repository.find_by_id(user_id)
        if not existing_user:
            return None
        
        # Validate partial data
        if 'email' in user_data:
            self._validate_email(user_data['email'])
            # Check email conflict
            existing_email = self.user_repository.find_by_email(user_data['email'])
            if existing_email and existing_email.id != user_id:
                raise ConflictError("Email already exists")
        
        if 'username' in user_data:
            self._validate_username(user_data['username'])
            # Check username conflict
            existing_username = self.user_repository.find_by_username(user_data['username'])
            if existing_username and existing_username.id != user_id:
                raise ConflictError("Username already exists")
        
        # Hash password if provided
        if 'password' in user_data:
            user_data['password'] = self._hash_password(user_data['password'])
        
        # Update user
        updated_user = self.user_repository.partial_update(user_id, user_data)
        return {"data": self._serialize_user(updated_user)}
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False if not found
        """
        return self.user_repository.delete(user_id)
    
    # Private helper methods
    
    def _serialize_user(self, user) -> Dict[str, Any]:
        """
        Serialize user object to dict, excluding sensitive data
        
        Args:
            user: User model object
            
        Returns:
            Serialized user data
        """
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    
    def _validate_user_data(self, user_data: Dict[str, Any]) -> None:
        """
        Validate complete user data
        
        Args:
            user_data: User data to validate
            
        Raises:
            ValueError: If validation fails
        """
        # Check required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValueError(f"{field} is required")
        
        # Validate individual fields
        self._validate_username(user_data['username'])
        self._validate_email(user_data['email'])
        self._validate_password(user_data['password'])
    
    def _validate_username(self, username: str) -> None:
        """Validate username format"""
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        if not username.replace('_', '').isalnum():
            raise ValueError("Username must contain only letters, numbers, and underscores")
    
    def _validate_email(self, email: str) -> None:
        """Validate email format"""
        import re
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
    
    def _validate_password(self, password: str) -> None:
        """Validate password strength"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
    
    def _check_conflicts(self, user_data: Dict[str, Any], exclude_id: int) -> None:
        """
        Check for username/email conflicts
        
        Args:
            user_data: User data to check
            exclude_id: User ID to exclude from conflict check
            
        Raises:
            ConflictError: If conflicts found
        """
        # Check username
        if 'username' in user_data:
            existing = self.user_repository.find_by_username(user_data['username'])
            if existing and existing.id != exclude_id:
                raise ConflictError("Username already exists")
        
        # Check email
        if 'email' in user_data:
            existing = self.user_repository.find_by_email(user_data['email'])
            if existing and existing.id != exclude_id:
                raise ConflictError("Email already exists")
    
    def _hash_password(self, password: str) -> str:
        """
        Hash password using bcrypt or similar
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        # In a real application, use bcrypt or argon2
        # This is a placeholder
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()


class ConflictError(Exception):
    """Raised when there's a conflict (e.g., duplicate username/email)"""
    pass
