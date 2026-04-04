"""
Tests for URL update endpoint.
Tests the /update POST endpoint in isolation.
"""

import pytest
import time


class TestURLUpdate:
    """Test suite for URL update functionality."""

    def test_update_title_success(self, client, sample_user, sample_url):
        """Test successful title update."""
        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': sample_url['id'],
            'field': 'title',
            'new_value': 'Updated Title'
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'URL updated successfully'
        assert data['field'] == 'title'
        assert data['new_value'] == 'Updated Title'
        assert 'old_value' in data

    def test_update_is_active_success(self, client, sample_user, sample_url):
        """Test successful is_active update."""
        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': sample_url['id'],
            'field': 'is_active',
            'new_value': False
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data['field'] == 'is_active'
        assert data['new_value'] == 'False'

    def test_update_original_url_success(self, client, sample_user, sample_url):
        """Test successful original_url update."""
        new_url = 'https://updated-example.com/new-path'

        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': sample_url['id'],
            'field': 'original_url',
            'new_value': new_url
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data['field'] == 'original_url'
        assert data['new_value'] == new_url

    def test_update_invalid_field(self, client, sample_user, sample_url):
        """Test update fails with invalid field name."""
        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': sample_url['id'],
            'field': 'short_code',  # Not allowed to change
            'new_value': 'NEWCODE'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'invalid field' in data['error'].lower() or 'allowed' in data['error'].lower()

    def test_update_missing_user_id(self, client, sample_url):
        """Test update fails when user_id is missing."""
        response = client.post('/update', json={
            'url_id': sample_url['id'],
            'field': 'title',
            'new_value': 'New Title'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_update_missing_url_id(self, client, sample_user):
        """Test update fails when url_id is missing."""
        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'field': 'title',
            'new_value': 'New Title'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_update_missing_field(self, client, sample_user, sample_url):
        """Test update fails when field is missing."""
        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': sample_url['id'],
            'new_value': 'New Value'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_update_missing_new_value(self, client, sample_user, sample_url):
        """Test update fails when new_value is missing."""
        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': sample_url['id'],
            'field': 'title'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_update_nonexistent_user(self, client, sample_url):
        """Test update fails with non-existent user."""
        response = client.post('/update', json={
            'user_id': 999999,
            'url_id': sample_url['id'],
            'field': 'title',
            'new_value': 'New Title'
        })

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_update_nonexistent_url(self, client, sample_user):
        """Test update fails with non-existent URL."""
        response = client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': 999999,
            'field': 'title',
            'new_value': 'New Title'
        })

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
