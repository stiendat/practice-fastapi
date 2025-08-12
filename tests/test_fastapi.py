import asyncio
import sys
import pytest
from fastapi.testclient import TestClient
from main import app


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


def test_create_todo(test_client):
    payload = {"title": "Test Todo"}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert "id" in data and isinstance(data["id"], str)
    assert data["title"] == "Test Todo"
    assert data["completed"] is False

    # Save id for later tests
    test_create_todo.todo_id = data["id"]


def test_create_todo_malformed_payload(test_client):
    # Missing 'title' field
    payload = {"completed": False}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 422

    # Title is not a string
    payload = {"title": 123}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 422


def test_get_todos(test_client):
    response = test_client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        todo = data[0]
        assert "id" in todo
        assert "title" in todo
        assert "completed" in todo
        assert "created_at" in todo
        assert "updated_at" in todo


def test_create_todo_with_extra_fields(test_client):
    payload = {"title": "Extra Fields", "extra": "should be ignored"}
    response = test_client.post("/todos", json=payload)
    # Should ignore extra fields and create todo
    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data and "title" in data and "completed" in data
    assert data["title"] == "Extra Fields"
    # Clean up
    test_client.delete(f"/todos/{data['id']}")


def test_update_todo(test_client):
    todo_id = getattr(test_create_todo, "todo_id", None)
    assert todo_id is not None, "No todo_id from create test"
    payload = {"title": "Updated Todo", "completed": True}
    response = test_client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated Todo"
    assert data["completed"] is True
    assert "updated_at" in data


def test_update_todo_partial_fields(test_client):
    # Create a new todo for this test
    payload = {"title": "Partial Update Todo"}
    response = test_client.post("/todos", json=payload)
    assert response.status_code in (200, 201)
    todo_id = response.json()["id"]

    # Update only the title
    payload = {"title": "Title Only Update"}
    response = test_client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Title Only Update"
    # Update only the completed field
    payload = {"completed": True}
    response = test_client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    # Clean up
    test_client.delete(f"/todos/{todo_id}")


def test_delete_todo(test_client):
    todo_id = getattr(test_create_todo, "todo_id", None)
    assert todo_id is not None, "No todo_id from create test"
    response = test_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Todo deleted successfully"}


def test_delete_unknown_todo(test_client):
    import uuid
    unknown_id = str(uuid.uuid4())
    response = test_client.delete(f"/todos/{unknown_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_nonexistent_todo(test_client):
    import uuid
    unknown_id = str(uuid.uuid4())
    payload = {"title": "Doesn't exist", "completed": False}
    response = test_client.put(f"/todos/{unknown_id}", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_todo_malformed_payload(test_client):
    # Create a todo to update
    payload = {"title": "To be malformed"}
    response = test_client.post("/todos", json=payload)
    todo_id = response.json()["id"]
    # Missing both fields
    response = test_client.put(f"/todos/{todo_id}", json={})
    assert response.status_code == 422
    # Wrong type
    response = test_client.put(f"/todos/{todo_id}", json={"title": 123, "completed": "nope"})
    assert response.status_code == 422
    # Clean up
    test_client.delete(f"/todos/{todo_id}")


def test_create_multiple_todos_and_list(test_client):
    ids = []
    for i in range(3):
        payload = {"title": f"Bulk {i}"}
        response = test_client.post("/todos", json=payload)
        ids.append(response.json()["id"])
    response = test_client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    titles = [todo["title"] for todo in data]
    for i in range(3):
        assert f"Bulk {i}" in titles
    # Clean up
    for id in ids:
        test_client.delete(f"/todos/{id}")


def test_delete_todo_twice(test_client):
    payload = {"title": "Delete Twice"}
    response = test_client.post("/todos", json=payload)
    todo_id = response.json()["id"]
    response = test_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    response = test_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 404


def test_timestamps_format(test_client):
    payload = {"title": "Check Timestamp"}
    response = test_client.post("/todos", json=payload)
    todo_id = response.json()["id"]
    response = test_client.get("/todos")
    todo = next(t for t in response.json() if t["id"] == todo_id)
    import re
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    assert re.match(pattern, todo["created_at"])
    assert re.match(pattern, todo["updated_at"])
    # Clean up
    test_client.delete(f"/todos/{todo_id}")


def test_update_todo_no_fields(test_client):
    payload = {"title": "No fields update"}
    response = test_client.post("/todos", json=payload)
    todo_id = response.json()["id"]
    response = test_client.put(f"/todos/{todo_id}", json={})
    assert response.status_code == 422
    test_client.delete(f"/todos/{todo_id}")


def test_create_todo_empty_title(test_client):
    payload = {"title": ""}
    response = test_client.post("/todos", json=payload)
    # Accept 422 or 200 depending on implementation
    assert response.status_code in (200, 201, 422)
    if response.status_code in (200, 201):
        # Clean up
        test_client.delete(f"/todos/{response.json()['id']}")


def test_case_sensitivity_in_title(test_client):
    payload1 = {"title": "CaseTest"}
    payload2 = {"title": "casetest"}
    r1 = test_client.post("/todos", json=payload1)
    r2 = test_client.post("/todos", json=payload2)
    assert r1.status_code in (200, 201)
    assert r2.status_code in (200, 201)
    id1 = r1.json()["id"]
    id2 = r2.json()["id"]
    assert id1 != id2
    test_client.delete(f"/todos/{id1}")
    test_client.delete(f"/todos/{id2}")
