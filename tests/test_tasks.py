from tests.conftest import TaskFactory


def test_create_task(client, token):
    response = client.post(
        '/tasks',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Task Test',
            'description': 'testing the task description',
            'state': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Task Test',
        'description': 'testing the task description',
        'state': 'draft',
    }


def test_list_tasks_should_return_5_tasks(session, client, user, token):
    expected_tasks = 5
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


def test_list_tasks_pagination_should_return_2_tasks(session, client, user, token):
    expected_tasks = 2
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/tasks/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks
