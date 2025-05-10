import pytest
from app import app
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# ----------------------------
# CRUD Operations
# ----------------------------

def test_put_key(client):
    res = client.post("/put", json={"key": "foo", "value": "bar"})
    assert res.status_code == 200

def test_get_key(client):
    client.post("/put", json={"key": "alpha", "value": "beta"})
    res = client.get("/get/alpha")
    assert res.status_code == 200
    assert res.json["value"] == "beta"

def test_delete_key(client):
    client.post("/put", json={"key": "temp", "value": "123"})
    client.delete("/delete/temp")
    res = client.get("/get/temp")
    assert res.json["value"] is None

# ----------------------------
# Metrics
# ----------------------------

def test_metrics_endpoint(client):
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "latency_ms_avg" in res.json

# ----------------------------
# Edge Cases
# ----------------------------

def test_empty_key(client):
    res = client.post("/put", json={"key": "", "value": "val"})
    assert res.status_code in [400, 200]

def test_empty_value(client):
    res = client.post("/put", json={"key": "key1", "value": ""})
    assert res.status_code == 200

def test_nonexistent_get(client):
    res = client.get("/get/notfound")
    assert res.status_code == 200
    assert res.json["value"] is None

# ----------------------------
# Massive Load
# ----------------------------

@pytest.mark.parametrize("i", range(40))
def test_massive_put_get(client, i):
    key = f"key{i}"
    value = f"val{i}"
    client.post("/put", json={"key": key, "value": value})
    res = client.get(f"/get/{key}")
    assert res.status_code == 200
    assert res.json["value"] == value

# ----------------------------
# Promotion Endpoint
# ----------------------------

def test_promote(client):
    res = client.post("/promote")
    assert res.status_code == 200

# ----------------------------
# Print Endpoint
# ----------------------------

def test_print(client):
    res = client.get("/print")
    assert res.status_code == 200
    assert isinstance(res.json, dict)

# ----------------------------
# Delete non-existent key
# ----------------------------

def test_delete_nonexistent(client):
    res = client.delete("/delete/nokey")
    assert res.status_code == 200