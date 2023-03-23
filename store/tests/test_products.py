from rest_framework import status
from model_bakery import baker
import pytest

from store.models import Product


@pytest.fixture
def create_product(api_client):
    def do_create_product(test_product):
        return api_client.post('/store/products/', test_product)
    return do_create_product


@pytest.mark.django_db
class TestCreateCollections:
    # TODO:
    @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, create_product):
        # AAA (Arrange , Act , Assert)
        # Arrange
        product = baker.make(Product)

        # Act
        response = create_product(product)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRetriveProducts:

    def test_if_product_exists_returns_200(self, api_client):
        # Arange
        product = baker.make(Product)

        # Act
        response = api_client.get(f'/store/products/{product.id}/')

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_if_product_not_exists_returns_404(self, api_client):
        # Act
        response = api_client.get(f'/store/products/{100}/')

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
