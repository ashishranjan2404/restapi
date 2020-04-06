from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_tasks_routes():
    task_id = 123123
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
