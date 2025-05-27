from django.test import TestCase
from django.contrib.auth import get_user
from django.urls import reverse, reverse_lazy

from users.models import CustomUser


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                "username": "sayitkamol",
                "first_name": "sayitkamol",
                "last_name": "azimjonov",
                "email": "sayitkamol@gmail.com",
                "password": "qiyinparol"
            }
        )

        user = CustomUser.objects.get(username='sayitkamol')

        self.assertEqual(user.first_name, 'sayitkamol')
        self.assertEqual(user.last_name, 'azimjonov')
        self.assertEqual(user.email, 'sayitkamol@gmail.com')
        self.assertNotEqual(user.password, 'qiyinparol')
        self.assertTrue(user.check_password('qiyinparol'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "sayitkamol",
                "email": "sayitkamol@gmail.com",
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response.context["form"], "username", "This field is required.")
        self.assertFormError(response.context["form"], "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "username": "sayitkamol",
                "first_name": "sayitkamol",
                "last_name": "azimjonov",
                "email": "sayitkamol-ail.com",
                "password": "qiyinparol"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response.context["form"], "email", "Enter a valid email address.")

    def test_unique_username(self):
        # 1. create a user
        user = CustomUser.objects.create_user(username='sayitkamol', email='sayitkamol@gmail.com')
        user.set_password('qiyinparol')
        user.save()

        # 2. try to create another user with that same username
        response = self.client.post(
            reverse('users:register'),
            data={
                "username": "sayitkamol",
                "first_name": "sayitkamol",
                "last_name": "azimjonov",
                "email": "sayitkamol@gmail.com",
                "password": "qiyinparol"
            }
        )

        # 3. check that the second user was not created
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        # 4. check that the form contains the error message
        self.assertFormError(response.context["form"], "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='sayitkamol', first_name='sayitkamol')
        self.db_user.set_password('qiyinp')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": "sayitkamol",
                "password": "qiyinp"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": "xato-sayitkamol",
                "password": "xatopas"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                "username": "sayitkamol",
                "password": "xatopas"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="sayitkamol", password='qiyinp')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + "?next=" + reverse('users:profile'))

    def test_profile_details(self):
        user1 = CustomUser.objects.create(
            username='sayitkamol',
            first_name='sayitkamol',
            last_name='azimjonov',
            email='sayitkamol@gmail.com'
        )
        user1.set_password("passqiyin")
        user1.save()

        self.client.login(username='sayitkamol', password='passqiyin')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user1.username)
        self.assertContains(response, user1.first_name)
        self.assertContains(response, user1.last_name)
        self.assertContains(response, user1.email)

    def test_update_profile(self):
        user1 = CustomUser.objects.create(
            username='sayitkamol',
            first_name='sayitkamol',
            last_name='azimjonov',
            email='sayitkamol@gmail.com'
        )
        user1.set_password("parol")
        user1.save()

        self.client.login(username='sayitkamol', password='parol')

        response = self.client.post(
            reverse("users:profile_edit"),
            data={
                "username": "jasur",
                "first_name": "jasur",
                "last_name": "ismoilov",
                "email": "jasurismoil@gmail.com",
            }
        )

        user1.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(user1.username, 'jasur')
        self.assertEqual(user1.first_name, 'jasur')
        self.assertEqual(user1.last_name, 'ismoilov')
        self.assertEqual(user1.email, 'jasurismoil@gmail.com')
        self.assertEqual(response.url, reverse("users:profile"))

