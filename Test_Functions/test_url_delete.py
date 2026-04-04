"""
Tests for URL deletion endpoint.
Tests the /delete POST endpoint in isolation.
"""

import pytest
import time


class TestURLDelete:
    """Test suite for URL deletion functionality."""

    def test_delete_url_success(self, client, sample_user, sample_url):
        """Test successful URL deletion."""
        response = client.post('/delete', json={
            'user_id': sample_user['id'],
            'title': sample_url['title']
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'URL deleted successfully'
        assert 'deleted_url' in data
        assert data['deleted_url']['url_id'] == sample_url['id']
        assert 'events_deleted' in data

    def test_delete_url_removes_from_database(self, client, sample_user, sample_url):
        """Test that deleted URL is actually removed from database."""
        # Delete the URL
        response = client.post('/delete', json={
            'user_id': sample_user['id'],
            'title': sample_url['title']
        })
        assert response.status_code == 200

        # Try to delete again - should fail
        response = client.post('/delete', json={
            'user_id': sample_user['id'],
            'title': sample_url['title']
        })
        assert response.status_code == 404

    def test_delete_url_missing_user_id(self, client, sample_url):
        """Test deletion fails when user_id is missing."""
        response = client.post('/delete', json={
            'title': sample_url['title']
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_delete_url_missing_title(self, client, sample_user):
        """Test deletion fails when title is missing."""
        response = client.post('/delete', json={
            'user_id': sample_user['id']
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_delete_url_nonexistent_user(self, client, sample_url):
        """Test deletion fails with non-existent user."""
        response = client.post('/delete', json={
            'user_id': 999999,
            'title': sample_url['title']
        })

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_delete_url_nonexistent_title(self, client, sample_user):
        """Test deletion fails with non-existent title."""
        response = client.post('/delete', json={
            'user_id': sample_user['id'],
            'title': 'This Title Does Not Exist'
        })

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_delete_url_wrong_user(self, client, sample_user, sample_url):
        """Test deletion fails when user doesn't own the URL."""
        # Create a different user
        timestamp = int(time.time() * 1000)
        response = client.post('/users', json={
            'username': f'otheruser_{timestamp}',
            'email': f'otheruser_{timestamp}@test.com'
        })
        other_user = response.get_json()

        # Try to delete URL owned by sample_user using other_user
        response = client.post('/delete', json={
            'user_id': other_user['id'],
            'title': sample_url['title']
        })

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_delete_url_deletes_events(self, client, sample_user):
        """Test that deleting a URL also deletes its events."""
        timestamp = int(time.time() * 1000)

        # Create a URL
        response = client.post('/shorten', json={
            'user_id': sample_user['id'],
            'original_url': f'https://example.com/event-delete-test/{timestamp}',
            'title': f'Event Delete Test {timestamp}'
        })
        url_data = response.get_json()

        # Update it to create more events
        client.post('/update', json={
            'user_id': sample_user['id'],
            'url_id': url_data['id'],
            'field': 'title',
            'new_value': 'Updated Event Delete Test'
        })

        # Delete the URL
        response = client.post('/delete', json={
            'user_id': sample_user['id'],
            'title': 'Updated Event Delete Test'
        })

        assert response.status_code == 200
        data = response.get_json()
        # Should have deleted at least 2 events (created + updated)
        assert data['events_deleted'] >= 2
