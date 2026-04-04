def test_health_endpoint(client):
    """Verify the /health endpoint returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
