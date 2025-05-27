from django.http import response
from django.test import TestCase
from django.shortcuts import reverse

from users.models import CustomUser
from .models import Book, BookReview


class BooksTestCase(TestCase):

    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title='book1', description='description1', isbn='1234234')
        book2 = Book.objects.create(title='book2', description='description2', isbn='2222222')
        book3 = Book.objects.create(title='book3', description='description3', isbn='3333333')
        user = CustomUser.objects.create(username='sayitkamol', first_name='sayitkamol', last_name='azimjonov',
                                         email='sayitkamol@gmail.com', )
        user.set_password('qiyinparol')
        user.save()
        self.client.login(username='sayitkamol', password='qiyinparol')

        response = self.client.get(reverse("books:list") + "?page_size=2")

        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book1.title)
        self.assertNotContains(response, book3)

    def test_detail_page(self):
        book = Book.objects.create(title='book1', description='description1', isbn='1234234')

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        # self.assertContains(response, book.isbn)

    def test_search_books(self):
        book1 = Book.objects.create(title='sport', description='description1', isbn='1234234')
        book2 = Book.objects.create(title='Shoe', description='description2', isbn='2222222')
        book3 = Book.objects.create(title='guite', description='description3', isbn='3333333')

        response = self.client.get(reverse("books:list") + "?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Shoe")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=guite")
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertContains(response, book3.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='sport', description='description1', isbn='1234234')
        user = CustomUser.objects.create(username='sayitkamol', first_name='sayitkamol', last_name='azimjonov', email='sayitkamol@gmail.com',)
        user.set_password('qiyinparol')
        user.save()

        self.client.login(username='sayitkamol', password='qiyinparol')

        self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 3,
            "comment": "Nice book"
        })
        book_review = BookReview.objects.all()

        self.assertEqual(book_review.count(), 1)
        self.assertEqual(book_review[0].stars_given, 3)
        self.assertEqual(book_review[0].comment, "Nice book")
        self.assertEqual(book_review[0].book, book)
        self.assertEqual(book_review[0].user, user)






