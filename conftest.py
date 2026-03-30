import os
os.environ.setdefault('TESTING', 'true')

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@1.com',
        password='asdasd112',
        name='test',
        phone='010-1234-5678',
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def client():
    client = APIClient()

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client