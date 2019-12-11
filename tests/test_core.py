def test_eb_health_check(client):
    retval = client.get("/api/v1/eb/health")
    assert retval.status_code == 200
