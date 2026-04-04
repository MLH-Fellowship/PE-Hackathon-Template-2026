"""
Tests for user creation endpoint.
Tests the /users POST endpoint in isolation.
"""

import pytest
import time


class TestUserCreation:
    """Test suite for user creation functionality."""

    def test_create_user_success(self, client):
        """Test successful user creation with valid data."""
        timestamp = int(time.time() * 1000)

        response = client.post('/users', json={
            'username': f'newuser_{timestamp}',
            'email': f'newuser_{timestamp}@test.com'
        })

        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['username'] == f'newuser_{timestamp}'
        assert data['email'] == f'newuser_{timestamp}@test.com'
        assert 'created_at' in data

    def test_create_user_missing_username(self, client):
        """Test user creation fails when username is missing."""
        response = client.post('/users', json={
            'email': 'test@test.com'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'username' in data['error'].lower() or 'required' in data['error'].lower()

    def test_create_user_missing_email(self, client):
        """Test user creation fails when email is missing."""
        response = client.post('/users', json={
            'username': 'testuser'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_create_user_missing_body(self, client):
        """Test user creation fails when request body is missing."""
        response = client.post('/users',
            content_type='application/json'
        )

        # Should return 400 Bad Request
        assert response.status_code == 400
        data = response.get_json()
        # Data might be None or contain error
        assert data is None or 'error' in data

    def test_create_user_duplicate_username(self, client, sample_user):
        """Test user creation fails with duplicate username."""
        response = client.post('/users', json={
            'username': sample_user['username'],
            'email': 'different@test.com'
        })

        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'username' in data['error'].lower()

    def test_create_user_duplicate_email(self, client, sample_user):
        """Test user creation fails with duplicate email."""
        response = client.post('/users', json={
            'username': 'differentuser',
            'email': sample_user['email']
        })

        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_get_user_by_id(self, client, sample_user):
        """Test retrieving a user by ID."""
        response = client.get(f"/users/{sample_user['id']}")

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == sample_user['id']
        assert data['username'] == sample_user['username']

    def test_get_user_not_found(self, client):
        """Test retrieving a non-existent user returns 404."""
        response = client.get('/users/999999')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
