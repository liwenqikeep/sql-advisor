from fastapi.testclient import TestClient
from main import app

client = TestClient(app)                # 对标 MockMvc

def test_create_and_get():
    resp = client.post("/tasks", json={"id": 0, "title": "学 Python"})
    assert resp.status_code == 200      # assert 语句直接断言，无需 assertThat
    task_id = resp.json()["id"]
    assert client.get(f"/tasks/{task_id}").json()["title"] == "学 Python"

def test_get_not_found():
    assert client.get("/tasks/99999").status_code == 404