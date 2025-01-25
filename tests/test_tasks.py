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
