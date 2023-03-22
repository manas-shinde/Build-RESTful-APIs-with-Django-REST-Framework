from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate_user(is_staff=False):
        api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate_user
