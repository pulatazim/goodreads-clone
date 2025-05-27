from django.test import TestCase
from django.shortcuts import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Test Book', description='Test description', isbn='123123123')
        user = CustomUser.objects.create(
            username='sayitkamol', first_name='sayitkamol', last_name='azimjonov', email='sayitkamol@gmail.com'
        )
        user.set_password('sayitkamol')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Very good")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Useful book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Nice book")

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
