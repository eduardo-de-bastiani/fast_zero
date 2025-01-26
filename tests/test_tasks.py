from fast_zero.models import TaskState
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


def test_list_tasks_filter_title_should_return_5_tasks(session, client, user, token):
    expected_tasks = 5
    # todas as 5 tasks terao o title 'Task Test'
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, title='Task Test')
    )
    session.commit()

    response = client.get(
        '/tasks/?title=Task Test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


def test_list_tasks_filter_description_should_return_5_tasks(
    session, client, user, token
):
    expected_tasks = 5

    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, description='Task description')
    )
    session.commit()

    response = client.get(
        # procurando so por um pedaco
        '/tasks/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


def test_list_tasks_filter_state_should_return_5_tasks(session, client, user, token):
    expected_tasks = 5

    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, state=TaskState.draft)
    )
    session.commit()

    response = client.get(
        '/tasks/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks


def test_list_tasks_filter_combined_should_return_5_tasks(session, user, client, token):
    # cria 8 tasks, mas filtra por apenas 5
    expected_tasks = 5
    
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5,
            user_id=user.id,
            title='Test task combined',
            description='combined description',
            state=TaskState.done,
        )
    )

    session.bulk_save_objects(
        TaskFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TaskState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/tasks/?title=Test task combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks
