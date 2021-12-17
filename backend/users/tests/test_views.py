from django.conf import settings
from django.test import TestCase, Client

from bonfix_utils.constants import Constants
from bonfix_utils.utils import generate_random_string, logger
from ..models import User, UserProfile

client = Client()
base_api_url = '/' + getattr(settings, "API_ROOT_URL_V1", 'api/v1/')
# for testing user account activation
user = None


class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        username = generate_random_string(8)
        data = {
            "email": f"{username}@test.com",
            "password": username,
            "profile": {"name": username},
        }
        response = client.post(path=base_api_url + "auth/signup", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(
            response.data["message"], "User registered successfully"
        )


class UserLoginTest(TestCase):
    def setUp(self):
        self.username = create_user_util()

    def test_user_login(self):
        # start test
        data = {
            "email": f"{self.username}@test.com",
            "password": {self.username},
        }
        response = client.post(path=base_api_url + "auth/signin", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], f"{self.username}@test.com")

    def test_user_login_unactivated(self):
        # deactivate account
        user.is_active = False
        user.save()
        # start test
        data = {
            "email": user.email,
            "password": {self.username},
        }
        response = client.post(path=base_api_url + "auth/signin", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'][0], Constants.ERROR_ACCOUNT_NOT_ACTIVATED)


class UserProfileTest(TestCase):
    def setUp(self):
        self.username = create_user_util()
        # create profile
        UserProfile.objects.create(user=user, name=self.username)
        # serializer = UserRegistrationSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        self.token = login(user.email, self.username)

    def test_user_profile(self):
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.token}",
        }
        response = client.get(path=base_api_url + "auth/profile", **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(
            response.data["message"], "User profile fetched successfully"
        )
        self.assertEqual(response.data["data"][0]["name"], self.username)


def create_user_util():
    global user
    username = generate_random_string(8)
    data = {
        "email": f"{username}@test.com",
        "password": username,
    }
    user = User.objects.create_user(**data)
    # activate account
    user.is_active = True
    user.save()
    return username


def login(email, password):
    response = client.post(path=base_api_url + "auth/signin", data={
        "email": email,
        "password": password,
    })
    return response.data["token"]
