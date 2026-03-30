import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

class TestUser:
    def test_create(self, user):
        assert user.id is not None
        assert user.email == 'test@1.com'

    def test_passowrd_is_hashed(self, user):
        assert user.password != "asdasd112"
        assert user.check_password("asdasd112")

    def test_read(self, user):
        found = User.objects.get(pk=user.pk)
        assert found.email == user.email

    def test_update(self, user):
        user.name = '변경 이름'
        user.save()
        assert User.objects.get(pk=user.pk).name == '변경 이름'

    def test_delete(self, user):
        pk = user.pk
        user.delete()
        assert not User.objects.filter(id=pk).exists()


class TestAuthAPI:
    def test_register(self, client, db):
        res = client.post("/api/users/register/",{
            "email": "new@1.com",
            "password": "asdasd112",
            "name": "test1",
            "phone": "010-1234-5678",
        })
        assert res.status_code == 201

    def test_login(self, client, user):
        res = client.post("/api/users/login/",{
            "email": "test@1.com",
            "password": "asdasd112",
        })
        assert res.status_code == 200
        assert "access" in res.cookies
        assert "refresh" in res.cookies

    def test_logout(self, client, user):
        # 로그인 해서 쿠키 세팅
        login_res = client.post("/api/users/login/",{
            "email": "test@1.com",
            "password": "asdasd112",
        })
        client.cookies = login_res.cookies

        res = client.post("/api/users/logout/")
        assert res.status_code == 200
        assert res.cookies["access"].value == ""
        assert res.cookies["refresh"].value == ""