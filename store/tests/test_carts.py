from rest_framework import status
from model_bakery import baker
import pytest

from store.models import Cart


@pytest.fixture
def create_cart(api_client):
    return api_client.post('/store/carts/', {})


@pytest.mark.django_db
class TestCreateCart:
    def test_if_user_is_anonymous_returns_200(self, create_cart):
        # Act
        response = create_cart

        # Assert
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetriveCart:
    def test_if_cart_exists_returns_200(self, api_client):
        cart = baker.make(Cart)

        response = api_client.get(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteCart:
    def test_if_existing_cart_delete_returns_204(self, api_client):
        cart = baker.make(Cart)

        response = api_client.delete(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
