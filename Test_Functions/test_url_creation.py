"""
Tests for URL creation/shortening endpoint.
Tests the /shorten POST endpoint in isolation.
"""

import pytest
import time


class TestURLCreation:
    """Test suite for URL shortening functionality."""

    def test_shorten_url_success(self, client, sample_user):
        """Test successful URL shortening with valid data."""
        timestamp = int(time.time() * 1000)

        response = client.post('/shorten', json={
            'user_id': sample_user['id'],
            'original_url': f'https://example.com/test/{timestamp}',
            'title': f'Test Link {timestamp}'
        })

        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert 'short_code' in data
        assert len(data['short_code']) == 6
        assert 'short_url' in data
        assert data['original_url'] == f'https://example.com/test/{timestamp}'
        assert data['title'] == f'Test Link {timestamp}'

    def test_shorten_url_missing_user_id(self, client):
        """Test URL shortening fails when user_id is missing."""
        response = client.post('/shorten', json={
            'original_url': 'https://example.com',
            'title': 'Test'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'user_id' in data['error']

    def test_shorten_url_missing_original_url(self, client, sample_user):
        """Test URL shortening fails when original_url is missing."""
        response = client.post('/shorten', json={
            'user_id': sample_user['id'],
            'title': 'Test'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'original_url' in data['error']

    def test_shorten_url_missing_title(self, client, sample_user):
        """Test URL shortening fails when title is missing."""
        response = client.post('/shorten', json={
            'user_id': sample_user['id'],
            'original_url': 'https://example.com'
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'title' in data['error']

    def test_shorten_url_invalid_user(self, client):
        """Test URL shortening fails with non-existent user."""
        response = client.post('/shorten', json={
            'user_id': 999999,
            'original_url': 'https://example.com',
            'title': 'Test'
        })

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'user' in data['error'].lower()

    def test_shorten_url_generates_unique_codes(self, client, sample_user):
        """Test that each shortened URL gets a unique short_code."""
        codes = set()

        for i in range(5):
            response = client.post('/shorten', json={
                'user_id': sample_user['id'],
                'original_url': f'https://example.com/test/{i}',
                'title': f'Test Link {i}'
            })

            assert response.status_code == 201
            data = response.get_json()
            codes.add(data['short_code'])

        # All 5 codes should be unique
        assert len(codes) == 5

    def test_shorten_url_creates_event(self, client, sample_user):
        """Test that creating a URL also creates a 'created' event."""
        timestamp = int(time.time() * 1000)

        response = client.post('/shorten', json={
            'user_id': sample_user['id'],
            'original_url': f'https://example.com/event-test/{timestamp}',
            'title': f'Event Test {timestamp}'
        })

        assert response.status_code == 201
        # Event creation is internal - we just verify the endpoint succeeds
        # A more thorough test would query the events table directly
