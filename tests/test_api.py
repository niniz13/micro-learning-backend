import django
import os
import pytest

os.environ['DJANGO_SETTINGS_MODULE'] = 'micro_learning.settings'
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(api_client):
    def _create_user(email="test@example.com", password="password123", authenticated=False):
        user = User.objects.create_user(email=email, password=password)
        if authenticated:
            refresh = RefreshToken.for_user(user)
            api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
            return user, api_client
        return user
    return _create_user

@pytest.mark.django_db
def test_update_user_profile(create_user):
    """Test modification du profil sans changer le mot de passe"""
    user, client = create_user(authenticated=True)
    url = f"/api/users/{user.id}/"

    response = client.patch(url, {"first_name": "NewName"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "NewName"

@pytest.mark.django_db
def test_update_password(create_user):
    """Test changement de mot de passe avec le bon mot de passe actuel"""
    user, client = create_user(authenticated=True)
    url = f"/api/users/{user.id}/"

    response = client.patch(url, {
        "current_password": "password123",
        "new_password": "newpassword456"
    }, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password("newpassword456")

@pytest.mark.django_db
def test_register_user(api_client):
    """Test enregistrement d'un nouvel utilisateur"""
    url = "/api/users/register/"

    response = api_client.post(url, {
        "email": "newuser@example.com",
        "password": "securepassword",
        "first_name": "John",
        "last_name": "Doe"
    }, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="newuser@example.com").exists()

@pytest.mark.django_db
def test_register_existing_email(create_user, api_client):
    """Test échec d'enregistrement avec un email déjà utilisé"""
    create_user(email="existing@example.com")
    url = "/api/users/register/"

    response = api_client.post(url, {
        "email": "existing@example.com",
        "password": "anotherpassword",
        "first_name": "Jane",
        "last_name": "Doe"
    }, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
