import os
from unittest.mock import patch

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from openoligo.api.helpers import update_task_status
from openoligo.api.models import TaskStatus
from openoligo.hal.platform import Platform
from openoligo.scripts.server import app, get_db_url
from openoligo.seq import SeqCategory

client = TestClient(app)


def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Operational"}


def test_get_all_tasks_in_synthesis_queue(db):
    response = client.get("/queue")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Add tasks to the queue with different statuses
    sequence1 = "AAATTT"
    sequence2 = "CCGG"
    category1 = SeqCategory.DNA.value
    category2 = SeqCategory.RNA.value
    rank1 = 0
    rank2 = 1
    status1 = TaskStatus.IN_PROGRESS
    status2 = TaskStatus.COMPLETE

    response1 = client.post(f"/queue?sequence={sequence1}&category={category1}&rank={rank1}")
    assert response1.status_code == 201, f"Unexpected response code: {response1.status_code}"
    response2 = client.post(f"/queue?sequence={sequence2}&category={category2}&rank={rank2}")
    assert response2.status_code == 201, f"Unexpected response code: {response2.status_code}"
    await update_task_status(1, status1)
    await update_task_status(2, status2)

    # Filter by status
    response = client.get(f"/queue?filter_by={status1.value}")
    assert response.status_code == 200, f"Unexpected response code: {response.status_code}"
    tasks = response.json()
    assert len(tasks) == 1, f"Expected 1 task, got {len(tasks)}"
    assert all(
        task["status"] == status1.value for task in tasks
    ), "Not all tasks have the expected status"


# @pytest.mark.asyncio
# async def test_get_tasks_by_filter(db):
#    sequence1 = "AAATTT"
#    sequence2 = "CCGG"
#    category1 = SeqCategory.DNA.value
#    category2 = SeqCategory.RNA.value
#    rank1 = 0
#    rank2 = 1
#    status1 = TaskStatus.IN_PROGRESS
#    status2 = TaskStatus.COMPLETE
#
#    # Add tasks to the queue with different statuses
#    response1 = client.post(f"/queue?sequence={sequence1}&category={category1}&rank={rank1}")
#    assert response1.status_code == 201, f"Unexpected response code: {response1.status_code}"
#    response2 = client.post(f"/queue?sequence={sequence2}&category={category2}&rank={rank2}")
#    assert response2.status_code == 201, f"Unexpected response code: {response2.status_code}"
#    await update_task_status(1, status1)
#    await update_task_status(2, status2)
#
#    # Filter by status
#    response = client.get(f"/queue?filter_by={status1.value}")
#    assert response.status_code == 200, f"Unexpected response code: {response.status_code}"
#    tasks = response.json()
#    assert len(tasks) == 1, f"Expected 1 task, got {len(tasks)}"
#    assert all(
#        task["status"] == status1.value for task in tasks
#    ), "Not all tasks have the expected status"


def test_clear_all_queued_tasks_in_task_queue(db):
    response = client.delete("/queue")
    assert response.status_code == 200


def test_get_task_by_id(db):
    client.post(f"/queue?sequence=AAATTT&category=DNA")
    client.post(f"/queue?sequence=CCGG&category=RNA&rank=1")

    # get the task
    response = client.get(f"/queue/2")
    assert response.status_code == 200
    assert response.json()["id"] == 2

    # get a task that doesn't exist
    response = client.get(f"/queue/100")
    assert response.status_code == 404
def test_clear_all_queued_tasks_in_task_queue(db):
    response = client.delete("/queue")
    assert response.status_code == 200


def test_get_task_by_id(db):
    client.post(f"/queue?sequence=AAATTT&category=DNA")
    client.post(f"/queue?sequence=CCGG&category=RNA&rank=1")

    # get the task
    response = client.get(f"/queue/2")
    assert response.status_code == 200
    assert response.json()["id"] == 2

    # get a task that doesn't exist
    response = client.get(f"/queue/100")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_a_synthesis_task(db):
    response1 = client.post("/queue?sequence=AAATTT&category=DNA")
    response2 = client.post("/queue?sequence=CCGG&category=DNA&rank=1")

    # extract the task ids from the responses
    task_id1 = response1.json()["id"]
    task_id2 = response2.json()["id"]

    # update the task
    updated_data = {"sequence": "GTCA", "rank": 2}

    # Try updating the task using the correct id
    response = client.put(f"/queue/{task_id2}", json=updated_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["sequence"] == "GTCA"

    # Try updating the task without providing the id
    response = client.put(f"/queue/", json=updated_data)
    assert response.status_code == 405

    # Try updating the task using the wrong id
    response = client.put(f"/queue/999999", json=updated_data)
    assert response.status_code == 404

    # Try updating the task that is already in progress, complete or failed
    await update_task_status(task_id1, TaskStatus.IN_PROGRESS)
    response = client.put(f"/queue/1", json=updated_data)
    assert response.status_code == 400

    response = client.put(f"/queue/2", json={"sequence": None, "rank": None})
    assert response.status_code == 400

    response = client.put(f"/queue/2", json={"sequence": "AG", "rank": 1})
    assert response.status_code == 400


def test_delete_synthesis_task_by_id(db):
    # first add a task
    response = client.post("/queue?sequence=ACTG&category=DNA&rank=1")
    task_id = response.json()["id"]
    # delete the task
    response = client.delete(f"/queue/{task_id}")
    assert response.status_code == 200

    # try deleting the task again
    response = client.delete(f"/queue/{task_id}")
    assert response.status_code == 404


@patch("os.path.expanduser")
def test_get_db_url(mock_expanduser):
    global tmp_dir  # Assuming tmp_dir is a global variable
    tmp_dir = "/tmp"

    # Setup the mock functions
    mock_expanduser.return_value = "/home/user/.openoligo"

    # Test the case when platform is RPI
    platform = Platform.RPI
    assert get_db_url(platform) == "sqlite:///tmp/openoligo/openoligo.db"

    # Test the case when platform is BB
    platform = Platform.BB
    assert get_db_url(platform) == "sqlite:///tmp/openoligo/openoligo.db"

    # Test the case when platform is anything else
    platform = Platform.SIM
    assert get_db_url(platform) == "sqlite:///home/user/.openoligo/openoligo.db"
