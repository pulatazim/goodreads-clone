from rest_framework import status
from rest_framework.test import APITestCase

from django.shortcuts import reverse

from users.models import CustomUser
from books.models import Book, BookReview


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='sayitkamol', first_name='sayitkamol')
        self.user.set_password('qiyinparol')
        self.user.save()
        self.client.login(username='sayitkamol', password='qiyinparol')

    def test_book_review_detail(self):
        book = Book.objects.create(title="book1", description="description1", isbn="12334543")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="very good")

        response = self.client.get(reverse("api:review-detail", kwargs={"id": br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['comment'], "very good")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'book1')
        self.assertEqual(response.data['book']['description'], 'description1')
        self.assertEqual(response.data['book']['isbn'], '12334543')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], "sayitkamol")
        self.assertEqual(response.data['user']['username'], "sayitkamol")

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username='jasur', first_name='Jasurbek')
        book = Book.objects.create(title="book1", description="description1", isbn="12334543")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=4, comment="very good")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=2, comment="Not good")

        response = self.client.get(reverse("api:review-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertEqual(response.data['results'][0]['id'], br_two.id)
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)

    def test_delete_review(self):
        book = Book.objects.create(title="book1", description="description1", isbn="12334543")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good")

        response = self.client.delete(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="book1", description="description1", isbn="12334543")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good")

        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}), data={"stars_given": 4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stars_given'], 4)

    def test_put_review(self):
        book = Book.objects.create(title="book1", description="description1", isbn="12334543")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good")

        response = self.client.put(reverse('api:review-detail', kwargs={'id': br.id}),
                                   data={"stars_given": 4, 'comment': "Not good", 'user_id': self.user.id, 'book_id': book.id})
        br.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['comment'], "Not good")

    def test_book_create_review(self):
        book = Book.objects.create(title="book1", description="description1", isbn="12334543")

        data = {
            "stars_given": 4,
            "comment": "very good",
            "user_id": self.user.id,
            "book_id": book.id
        }
        response = self.client.post(reverse('api:review-list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stars_given'], 4)
        self.assertEqual(response.data['comment'], "very good")
        self.assertEqual(response.data['user']['id'], br.user.id)
