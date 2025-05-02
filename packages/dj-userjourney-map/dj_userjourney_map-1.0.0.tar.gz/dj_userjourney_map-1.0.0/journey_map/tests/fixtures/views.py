import pytest
from django.views import View
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to initialize the Django REST Framework APIClient for testing.

    :return: An instance of APIClient to make HTTP requests in tests.
    """
    return APIClient()


@pytest.fixture
def view():
    return View()
