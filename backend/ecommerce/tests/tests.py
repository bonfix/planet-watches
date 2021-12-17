from django.conf import settings
from django.test import TestCase, Client

from bonfix_utils.utils import generate_random_string, logger
from ecommerce.models import Product
from users.models import User

client = Client()
base_api_url = '/' + getattr(settings, "API_ROOT_URL_V1", 'api/v1/')
ecommerce_api = base_api_url + "ecommerce/"
# for caching login token
_token = None


class ProductsTest(TestCase):
    def setUp(self) -> None:
        # add some products
        Product.objects.create(is_active=1, created_at='2021-12-14 15:03:45.118794', quantity=9,
                               updated_at='2021-12-14 15:03:45.118794',
                               image='',
                               name='CLASSIC WATCH', price=123)
        Product.objects.create(is_active=1, created_at='2021-12-14 15:03:45.118794', quantity=9,
                               updated_at='2021-12-14 15:03:45.118794',
                               image='',
                               name='OLD WATCH', price=95)

    def test_get_products(self):
        response = client.get(ecommerce_api + 'products', **get_authorization_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


def get_login_token():
    global _token
    if _token is None:
        username = generate_random_string(8)
        data = {
            "email": f"{username}@test.com",
            "password": username,
        }
        user = User.objects.create_user(**data)
        # activate account
        user.is_active = True
        user.save()
        response = client.post(path=base_api_url + "auth/signin", data=data)
        _token = response.data["token"]
    return _token


def get_authorization_headers():
    return {"HTTP_AUTHORIZATION": f"Bearer {get_login_token()}"}
